import streamlit as st
import pandas as pd
import plotly.express as px
from pyathena import connect

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Radar Gerencial de Anomalías",
    page_icon="🌹",
    layout="wide"
)

# =====================================================
# ATHENA
# =====================================================

@st.cache_resource
def get_connection():

    return connect(
        s3_staging_dir="s3://flores-el-olor-mtt/athena-results/",
        region_name="us-east-1",
        schema_name="flores_el_olor"
    )

conn = get_connection()

# =====================================================
# HELPER
# =====================================================

@st.cache_data(ttl=300)
def ejecutar_query(sql):
    return pd.read_sql(sql, conn)

# =====================================================
# QUERIES
# =====================================================

QUERY_PRODUCCION = """
SELECT
    f.nombre AS finca,

    SUM(e.tallos_exportacion) AS tallos_exportados,

    (
        SUM(lp.esquejes_sembrados)
        -
        SUM(e.tallos_exportacion)
    ) AS perdidas,

    ROUND(
        (
            (
                SUM(lp.esquejes_sembrados)
                -
                SUM(e.tallos_exportacion)
            ) * 100.0
        )
        /
        NULLIF(
            SUM(lp.esquejes_sembrados),
            0
        ),
        2
    ) AS porcentaje_perdida

FROM flores_el_olor.lotes_produccion lp

JOIN flores_el_olor.fincas f
    ON lp.id_finca = f.id_finca

JOIN flores_el_olor.empaque e
    ON lp.id_lote = e.id_lote

GROUP BY f.nombre
"""

QUERY_COSTOS = """
SELECT
    f.nombre AS finca,

    SUM(c.costo_total_cop) AS costo_total,

    SUM(e.tallos_exportacion) AS tallos_exportados,

    ROUND(
        SUM(c.costo_total_cop)
        /
        NULLIF(
            SUM(e.tallos_exportacion),
            0
        ),
        2
    ) AS costo_por_tallo

FROM flores_el_olor.costos c

JOIN flores_el_olor.fincas f
    ON c.id_finca = f.id_finca

JOIN flores_el_olor.empaque e
    ON c.id_lote = e.id_lote

GROUP BY f.nombre
"""

QUERY_DEPENDENCIA = """
SELECT
    p.pais,

    SUM(ex.valor_facturado_usd)
        AS valor_facturado,

    ROUND(
        (
            SUM(ex.valor_facturado_usd) * 100.0
        )
        /
        SUM(
            SUM(ex.valor_facturado_usd)
        ) OVER(),
        2
    ) AS porcentaje

FROM flores_el_olor.exportaciones ex

JOIN flores_el_olor.pedidos p
    ON ex.id_pedido = p.id_pedido

GROUP BY p.pais
"""

QUERY_VARIEDADES = """
SELECT

    v.nombre AS variedad,

    (
        SUM(lp.esquejes_sembrados)
        -
        SUM(e.tallos_exportacion)
    ) AS perdidas,

    COALESCE(
        SUM(ex.valor_facturado_usd),
        0
    ) AS ingreso_generado

FROM flores_el_olor.variedades v

JOIN flores_el_olor.lotes_produccion lp
    ON v.id_variedad = lp.id_variedad

JOIN flores_el_olor.empaque e
    ON lp.id_lote = e.id_lote

LEFT JOIN flores_el_olor.pedidos p
    ON p.id_variedad = v.id_variedad

LEFT JOIN flores_el_olor.exportaciones ex
    ON ex.id_pedido = p.id_pedido

GROUP BY v.nombre
"""

QUERY_RIESGO = """
SELECT

    month AS mes,

    SUM(produccion_proyectada_tallos)
        AS produccion_proyectada,

    SUM(demanda_proyectada_tallos)
        AS demanda_proyectada

FROM flores_el_olor.forecast_2027

GROUP BY month

ORDER BY month
"""

# =====================================================
# DATA
# =====================================================

try:

    df_produccion = ejecutar_query(QUERY_PRODUCCION)
    df_costos = ejecutar_query(QUERY_COSTOS)
    df_dependencia = ejecutar_query(QUERY_DEPENDENCIA)
    df_variedades = ejecutar_query(QUERY_VARIEDADES)
    df_riesgo = ejecutar_query(QUERY_RIESGO)

except Exception as e:

    st.error("Error conectando con Athena")
    st.code(str(e))
    st.stop()

# =====================================================
# LIMPIEZA
# =====================================================

for df in [
    df_produccion,
    df_costos,
    df_dependencia,
    df_variedades,
    df_riesgo
]:
    df.fillna(0, inplace=True)

# =====================================================
# HEADER
# =====================================================

st.title("Radar Gerencial de Anomalías")
st.subheader("Flores El Olor S.A.S.")

st.info(
    """
    Dashboard conectado directamente a Amazon Athena sobre
    los datos almacenados en Amazon S3.
    """
)

# =====================================================
# KPIS
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Mayor Costo por Tallo",
        round(float(df_costos["costo_por_tallo"].max()), 2)
    )

with col2:
    st.metric(
        "Dependencia Comercial (%)",
        round(float(df_dependencia["porcentaje"].max()), 2)
    )

with col3:
    meses_riesgo = len(
        df_riesgo[
            df_riesgo["demanda_proyectada"]
            >
            df_riesgo["produccion_proyectada"]
        ]
    )

    st.metric(
        "Meses en Riesgo",
        meses_riesgo
    )

st.divider()

# =====================================================
# GRAFICO 1
# =====================================================

st.subheader("Producción vs Pérdidas")

fig1 = px.scatter(
    df_produccion,
    x="porcentaje_perdida",
    y="tallos_exportados",
    size="perdidas",
    color="finca",
    hover_name="finca"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# =====================================================
# GRAFICO 2
# =====================================================

st.subheader("Costo por Tallo Exportado")

fig2 = px.bar(
    df_costos,
    x="finca",
    y="costo_por_tallo",
    color="finca"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# =====================================================
# GRAFICO 3
# =====================================================

st.subheader("Variedades Problemáticas")

fig3 = px.scatter(
    df_variedades,
    x="perdidas",
    y="ingreso_generado",
    color="variedad"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# =====================================================
# GRAFICO 4
# =====================================================

st.subheader("Dependencia Comercial")

fig4 = px.treemap(
    df_dependencia,
    path=["pais"],
    values="valor_facturado"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# =====================================================
# GRAFICO 5
# =====================================================

st.subheader("Riesgo de Desabastecimiento 2027")

fig5 = px.line(
    df_riesgo,
    x="mes",
    y=[
        "produccion_proyectada",
        "demanda_proyectada"
    ],
    markers=True
)

st.plotly_chart(
    fig5,
    use_container_width=True
)