import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="Radar Gerencial de Anomalías",
    page_icon="🌹",
    layout="wide"
)

# =====================================================
# FUNCIONES
# =====================================================

@st.cache_data
def cargar_datos():

    produccion = pd.read_csv(
        "data/produccion_perdidas.csv"
    )

    costos = pd.read_csv(
        "data/costos_por_tallo.csv"
    )

    dependencia = pd.read_csv(
        "data/dependencia_comercial.csv"
    )

    variedades = pd.read_csv(
        "data/variedades_problematicas.csv"
    )

    riesgo = pd.read_csv(
        "data/riesgo_2027.csv"
    )

    return (
        produccion,
        costos,
        dependencia,
        variedades,
        riesgo
    )


def limpiar_dataframe(df):

    df = df.copy()

    df.replace(
        ["", "NULL", "null", "NaN", "nan"],
        pd.NA,
        inplace=True
    )

    df.fillna(0, inplace=True)

    return df


def convertir_numerico(df, columnas):

    for col in columnas:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            ).fillna(0)

    return df


# =====================================================
# CARGA DATOS
# =====================================================

try:

    (
        df_produccion,
        df_costos,
        df_dependencia,
        df_variedades,
        df_riesgo
    ) = cargar_datos()

    df_produccion = limpiar_dataframe(df_produccion)
    df_costos = limpiar_dataframe(df_costos)
    df_dependencia = limpiar_dataframe(df_dependencia)
    df_variedades = limpiar_dataframe(df_variedades)
    df_riesgo = limpiar_dataframe(df_riesgo)

    df_produccion = convertir_numerico(
        df_produccion,
        [
            "tallos_exportados",
            "perdidas",
            "porcentaje_perdida"
        ]
    )

    df_costos = convertir_numerico(
        df_costos,
        [
            "costo_total",
            "tallos_exportados",
            "costo_por_tallo"
        ]
    )

    df_dependencia = convertir_numerico(
        df_dependencia,
        [
            "valor_facturado",
            "porcentaje"
        ]
    )

    df_variedades = convertir_numerico(
        df_variedades,
        [
            "perdidas",
            "ingreso_generado"
        ]
    )

    df_riesgo = convertir_numerico(
        df_riesgo,
        [
            "produccion_proyectada",
            "demanda_proyectada"
        ]
    )

except Exception as e:

    st.error("Error cargando los archivos CSV.")
    st.code(str(e))
    st.stop()

# =====================================================
# HEADER
# =====================================================

st.title("🌹 Radar Gerencial de Anomalías")
st.subheader("Flores El Olor S.A.S.")

st.info(
    """
    Las visualizaciones fueron generadas a partir de consultas SQL
    ejecutadas previamente en Amazon Athena sobre los datos
    almacenados en Amazon S3.

    Los resultados fueron exportados desde Athena y utilizados
    como fuente de datos para este dashboard.
    """
)

# =====================================================
# KPIS
# =====================================================

st.header("Indicadores Gerenciales")

col1, col2, col3 = st.columns(3)

with col1:

    try:

        finca_mayor_costo = (
            df_costos.sort_values(
                by="costo_por_tallo",
                ascending=False
            )
            .iloc[0]
        )

        st.metric(
            "Mayor Costo por Tallo",
            round(
                float(
                    finca_mayor_costo["costo_por_tallo"]
                ),
                2
            )
        )

    except Exception:

        st.metric(
            "Mayor Costo por Tallo",
            "N/D"
        )

with col2:

    try:

        pais_principal = (
            df_dependencia.sort_values(
                by="porcentaje",
                ascending=False
            )
            .iloc[0]
        )

        st.metric(
            "Dependencia Comercial (%)",
            round(
                float(
                    pais_principal["porcentaje"]
                ),
                2
            )
        )

    except Exception:

        st.metric(
            "Dependencia Comercial (%)",
            "N/D"
        )

with col3:

    try:

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

    except Exception:

        st.metric(
            "Meses en Riesgo",
            "N/D"
        )

st.divider()

# =====================================================
# GRÁFICO 1
# =====================================================

st.subheader("Producción vs Pérdidas")

st.markdown(
    """
    Cada punto representa una finca.
    """
)

try:

    fig1 = px.scatter(
        df_produccion,
        x="porcentaje_perdida",
        y="tallos_exportados",
        color="finca",
        size="perdidas",
        hover_name="finca"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

except Exception as e:

    st.warning(
        f"No fue posible generar este gráfico: {e}"
    )

# =====================================================
# GRÁFICO 2
# =====================================================

st.subheader("Costo por Tallo Exportado")

try:

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

except Exception as e:

    st.warning(
        f"No fue posible generar este gráfico: {e}"
    )

# =====================================================
# GRÁFICO 3
# =====================================================

st.subheader("Variedades Problemáticas")

try:

    fig3 = px.scatter(
        df_variedades,
        x="perdidas",
        y="ingreso_generado",
        color="variedad",
        hover_name="variedad"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

except Exception as e:

    st.warning(
        f"No fue posible generar este gráfico: {e}"
    )

# =====================================================
# GRÁFICO 4
# =====================================================

st.subheader("Dependencia Comercial")

try:

    fig4 = px.treemap(
        df_dependencia,
        path=["pais"],
        values="valor_facturado"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

except Exception as e:

    st.warning(
        f"No fue posible generar este gráfico: {e}"
    )

# =====================================================
# GRÁFICO 5
# =====================================================

st.subheader("Riesgo de Desabastecimiento 2027")

try:

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

except Exception as e:

    st.warning(
        f"No fue posible generar este gráfico: {e}"
    )

# =====================================================
# TABLA DE RIESGOS
# =====================================================

st.subheader(
    "Meses donde la demanda supera la producción"
)

try:

    riesgos = df_riesgo[
        df_riesgo["demanda_proyectada"]
        >
        df_riesgo["produccion_proyectada"]
    ]

    st.dataframe(
        riesgos,
        use_container_width=True
    )

except Exception as e:

    st.warning(
        f"No fue posible mostrar la tabla: {e}"
    )

# =====================================================
# DATOS CRUDOS
# =====================================================

with st.expander("Ver datos utilizados"):

    try:
        st.write("Producción")
        st.dataframe(df_produccion)

        st.write("Costos")
        st.dataframe(df_costos)

        st.write("Dependencia Comercial")
        st.dataframe(df_dependencia)

        st.write("Variedades")
        st.dataframe(df_variedades)

        st.write("Riesgo 2027")
        st.dataframe(df_riesgo)

    except Exception:
        pass

# =====================================================
# CONCLUSIÓN
# =====================================================

st.divider()

st.subheader("Conclusión Gerencial")

st.write(
    """
    El análisis permite identificar diferencias relevantes
    entre las fincas productivas, especialmente en términos
    de pérdidas y costos operativos.

    También se observan variedades cuyo aporte económico
    resulta inferior al impacto de las pérdidas registradas.

    Finalmente, las proyecciones para 2027 muestran periodos
    donde la demanda esperada supera la capacidad productiva
    proyectada, situación que merece seguimiento preventivo.
    """
)