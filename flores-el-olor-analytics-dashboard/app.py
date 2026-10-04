import streamlit as st
import pandas as pd
import plotly.express as px
from pyathena import connect

# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="Radar Gerencial de Anomalías",
    page_icon="🌹",
    layout="wide"
)

# =====================================================
# CONEXIÓN ATHENA
# =====================================================

@st.cache_resource
def get_connection():
    return connect(
        s3_staging_dir="s3://flores-el-olor-mtt/athena-results/",
        region_name="us-east-1"
    )

conn = get_connection()


@st.cache_data(ttl=300)
def ejecutar_query(sql):
    return pd.read_sql(sql, conn)

# =====================================================
# CONSULTAS
# =====================================================

QUERY_INEFICIENCIA = """
SELECT *
FROM vw_indice_ineficiencia
"""

QUERY_DEPENDENCIA = """
SELECT *
FROM vw_dependencia_comercial
"""

QUERY_PRODUCCION_PERDIDAS = """
SELECT *
FROM vw_produccion_perdidas
"""

QUERY_VARIEDADES = """
SELECT *
FROM vw_variedades_problematicas
"""

QUERY_FORECAST = """
SELECT *
FROM vw_riesgo_2027
"""

# =====================================================
# CARGA DATOS
# =====================================================

try:

    df_ineficiencia = ejecutar_query(QUERY_INEFICIENCIA)
    df_dependencia = ejecutar_query(QUERY_DEPENDENCIA)
    df_produccion = ejecutar_query(QUERY_PRODUCCION_PERDIDAS)
    df_variedades = ejecutar_query(QUERY_VARIEDADES)
    df_forecast = ejecutar_query(QUERY_FORECAST)

except Exception as e:

    st.error("Error conectando con Athena")
    st.code(str(e))
    st.stop()

# =====================================================
# HEADER
# =====================================================

st.title("🌹 Radar Gerencial de Anomalías")
st.subheader("Flores El Olor S.A.S.")

st.info(
    """
    Este dashboard consulta información directamente desde Amazon Athena.
    Los datos analizados permanecen almacenados en Amazon S3 de acuerdo con
    la arquitectura construida durante el examen.
    """
)

# =====================================================
# KPIS
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Mayor Índice de Ineficiencia",
        round(df_ineficiencia["indice_ineficiencia"].max(), 2)
    )

with col2:
    st.metric(
        "Dependencia Comercial (%)",
        round(df_dependencia["porcentaje"].max(), 2)
    )

with col3:
    meses_riesgo = len(
        df_forecast[
            df_forecast["demanda_proyectada"]
            >
            df_forecast["produccion_proyectada"]
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

st.markdown(
    """
    Cada punto representa una finca.
    Los cuadrantes superiores permiten identificar operaciones que
    presentan simultáneamente altos costos y elevados porcentajes de pérdida.
    """
)

fig1 = px.scatter(
    df_produccion,
    x="porcentaje_perdida",
    y="costo_por_tallo",
    size="tallos_exportados",
    color="finca",
    hover_name="finca"
)

st.plotly_chart(fig1, use_container_width=True)

# =====================================================
# GRAFICO 2
# =====================================================

st.subheader("Variedades Problemáticas")

st.markdown(
    """
    Se comparan pérdidas registradas contra ingresos generados.
    """
)

fig2 = px.scatter(
    df_variedades,
    x="plantas_perdidas",
    y="ingreso_generado",
    color="variedad",
    hover_name="variedad"
)

st.plotly_chart(fig2, use_container_width=True)

# =====================================================
# GRAFICO 3
# =====================================================

st.subheader("Dependencia de Mercados")

fig3 = px.treemap(
    df_dependencia,
    path=["pais"],
    values="valor_facturado"
)

st.plotly_chart(fig3, use_container_width=True)

# =====================================================
# GRAFICO 4
# =====================================================

st.subheader("Riesgo de Desabastecimiento 2027")

fig4 = px.line(
    df_forecast,
    x="mes",
    y=[
        "produccion_proyectada",
        "demanda_proyectada"
    ],
    markers=True
)

st.plotly_chart(fig4, use_container_width=True)

# =====================================================
# CONCLUSIÓN
# =====================================================

st.divider()

st.subheader("Conclusión Gerencial")

st.write(
    """
    Se identifican diferencias significativas entre las fincas analizadas.

    Algunas operaciones presentan niveles de pérdida elevados respecto a
    su desempeño productivo, mientras que determinadas variedades generan
    pérdidas importantes en comparación con su aporte económico.

    La proyección para 2027 evidencia periodos donde la demanda estimada
    supera la capacidad productiva proyectada, situación que merece
    seguimiento preventivo por parte de la gerencia.
    """
)
