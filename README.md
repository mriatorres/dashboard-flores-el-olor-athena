# Radar Gerencial de Anomalías
![](https://github.com/mriatorres/dashboard-flores-el-olor-athena/blob/main/flores-el-olor-analytics-dashboard/images/pikachuflor.gif)
## Flores El Olor S.A.S.

Aplicación web desarrollada como componente analítico del examen práctico de Arquitecturas de Nube y Big Data.

La solución transforma la información almacenada en Amazon S3 y consultada mediante Amazon Athena en indicadores y visualizaciones orientadas a la toma de decisiones gerenciales.

El enfoque principal no consiste en mostrar únicamente métricas de producción o ventas, sino en identificar comportamientos atípicos, diferencias operativas y riesgos que merecen atención por parte de la gerencia.

---

# Objetivo

Construir una aplicación web que consuma la arquitectura desarrollada durante el examen y permita visualizar información relevante para el negocio de manera clara e interactiva.

La aplicación busca responder preguntas como:

- ¿Qué fincas presentan comportamientos anormales?
- ¿Dónde existen pérdidas desproporcionadas?
- ¿Qué mercados representan un riesgo por dependencia comercial?
- ¿Existen riesgos de desabastecimiento en las proyecciones futuras?
- ¿Qué situaciones requieren revisión inmediata por parte de la gerencia?

---

# Arquitectura utilizada

```text
                 Amazon S3
        ┌──────────┼──────────┐
        │          │          │
      raw       curated   athena-results
        │
        ▼

           Amazon Athena
        (motor de consulta)

                │
                ▼

          Streamlit App

                │
                ▼

        Dashboard Web

                │
                ▼

          URL Pública
```

---

# Tecnologías utilizadas

- Python
- Streamlit
- Pandas
- Plotly
- Amazon S3
- Amazon Athena
- AWS Glue Catalog
- PyAthena
- Boto3
- GitHub

---

# Estructura del proyecto

```text
flores-el-olor-analytics-dashboard
│
├── app.py
├── consultas.sql
├── requirements.txt
├── README.md
├── aws_config.py
└── .gitignore
```

---

# Indicadores implementados

## Índice de Ineficiencia

Relaciona los costos registrados con los ingresos generados.

Permite identificar operaciones donde los costos crecen más rápido que la rentabilidad obtenida.

Interpretación:

- Valores bajos indican mejor desempeño.
- Valores altos sugieren operaciones que requieren revisión.

---

## Dependencia Comercial

Mide qué porcentaje de los ingresos depende del principal mercado comprador.

Interpretación:

- Una alta concentración implica mayor riesgo comercial.
- Una distribución equilibrada reduce la dependencia externa.

---

## Riesgo de Desabastecimiento 2027

Compara la producción proyectada y la demanda proyectada.

Interpretación:

- Cuando la demanda supera la producción existe riesgo de incumplimiento.
- Estos casos son resaltados visualmente para facilitar el análisis.

---

# Visualizaciones

## Producción vs Pérdidas

Gráfico de dispersión donde cada punto representa una finca.

Variables visualizadas:

- Porcentaje de pérdida
- Costo por tallo
- Volumen exportado

Objetivo:

Identificar fincas con combinaciones atípicas de costos, pérdidas y producción.

---

## Variedades Problemáticas

Relaciona las pérdidas registradas con el ingreso generado por cada variedad.

Objetivo:

Detectar variedades que generan alta afectación operativa y bajo aporte económico.

---

## Dependencia de Mercados

Visualización de la distribución de ingresos por país.

Objetivo:

Determinar si la organización depende excesivamente de uno o pocos mercados.

---

## Riesgo de Desabastecimiento 2027

Comparación temporal entre:

- Producción proyectada
- Demanda proyectada

Objetivo:

Anticipar posibles problemas futuros de abastecimiento.

---

# Ejecución local

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar aplicación:

```bash
streamlit run app.py
```

La aplicación quedará disponible en:

```text
http://localhost:8501
```

---

# Configuración AWS

La aplicación requiere acceso a:

- Amazon S3
- Amazon Athena
- AWS Glue Catalog

La conexión se realiza mediante PyAthena.

Ejemplo:

```python
from pyathena import connect

conn = connect(
    s3_staging_dir="s3://athena-results/",
    region_name="us-east-1"
)
```

---

# Evidencias

## Arquitectura implementada

Agregar captura de:

- Bucket S3
- Carpetas raw
- curated
- athena-results

---

## Athena

Agregar captura de:

- Base de datos
- Tablas externas
- Consultas SQL ejecutadas

---

## Dashboard

Agregar captura de:

- Indicadores
- Visualizaciones
- Conclusión gerencial

---

## Aplicación desplegada

URL pública:

[Agregar URL del dashboard]

---

# Conclusión gerencial

El análisis permite identificar situaciones que no son evidentes mediante indicadores tradicionales de producción o ventas.

Las visualizaciones destacan comportamientos anómalos relacionados con pérdidas productivas, dependencia comercial y riesgos de abastecimiento proyectados para 2027.

La aplicación transforma información proveniente del Data Lake en conocimiento útil para apoyar la toma de decisiones estratégicas y operativas.

---

# Autor

María Fernanda Toro Torres

Ingeniería en Inteligencia Artificial y Ciencia de Datos

Universidad Pontificia Bolivariana

2026
