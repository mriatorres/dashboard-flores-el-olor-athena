# Radar Gerencial de Anomalías
![](https://github.com/mriatorres/dashboard-flores-el-olor-athena/blob/main/flores-el-olor-analytics-dashboard/images/pikachuflor.gif)
## Flores El Olor S.A.S.

Dashboard analítico desarrollado para el examen práctico de Arquitecturas de Nube y Big Data.

La aplicación transforma los resultados obtenidos mediante consultas SQL ejecutadas en Amazon Athena en visualizaciones interactivas orientadas a apoyar la toma de decisiones gerenciales.

El enfoque del análisis se centra en la identificación de anomalías operativas, riesgos productivos, dependencia comercial y oportunidades de mejora dentro del proceso productivo de Flores El Olor S.A.S.

---

# Objetivo

Desarrollar una aplicación web capaz de visualizar información relevante obtenida desde la arquitectura construida durante el examen.

El dashboard busca responder preguntas como:

- ¿Qué fincas presentan niveles atípicos de pérdida?
- ¿Cuáles son las operaciones menos eficientes?
- ¿Existe dependencia excesiva de ciertos mercados?
- ¿Qué variedades generan pérdidas elevadas?
- ¿Existen riesgos futuros de desabastecimiento?

---

# Contexto del proyecto

Durante el examen se construyó una arquitectura de datos utilizando:

- Amazon S3
- AWS Glue Catalog
- Amazon Athena

Los datos históricos de la empresa fueron almacenados en Amazon S3 y posteriormente consultados mediante Amazon Athena.

Los resultados de dichas consultas fueron exportados utilizando el mecanismo estándar de resultados de Athena para ser consumidos por esta aplicación web.

---

# Arquitectura utilizada

```text
Datos históricos
       │
       ▼

 Amazon S3
(raw / curated)

       │
       ▼

 AWS Glue Catalog

       │
       ▼

 Amazon Athena

       │
       ▼

 Athena Results

       │
       ▼

 Dashboard Streamlit

       │
       ▼

 GitHub + URL Pública
```

---

# Origen de los datos

Las visualizaciones mostradas en este dashboard fueron construidas a partir de resultados obtenidos mediante consultas SQL ejecutadas previamente en Amazon Athena.

El flujo seguido fue:

1. Construcción del Data Lake en Amazon S3.
2. Creación de tablas externas en Athena.
3. Ejecución de consultas SQL analíticas.
4. Generación de resultados en la ubicación configurada de Athena.
5. Descarga 