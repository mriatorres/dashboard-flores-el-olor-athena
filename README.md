# Radar Gerencial de Anomalías

![](https://github.com/mriatorres/dashboard-flores-el-olor-athena/blob/main/flores-el-olor-analytics-dashboard/images/pikachuflor.gif)

---

## Flores El Olor S.A.S.

Radar Gerencial de Anomalías es una aplicación web analítica desarrollada como parte del examen práctico de Arquitecturas de Nube y Big Data.

La solución permite analizar información operacional, productiva y comercial de la empresa ficticia Flores El Olor S.A.S., transformando datos almacenados en un Data Lake de AWS en información útil para la toma de decisiones.

La aplicación consulta información en tiempo real desde Amazon Athena y presenta los resultados mediante visualizaciones interactivas desarrolladas con Streamlit y Plotly.

![](https://github.com/mriatorres/dashboard-flores-el-olor-athena/blob/main/flores-el-olor-analytics-dashboard/images/radargerencial.png)
![](https://github.com/mriatorres/dashboard-flores-el-olor-athena/blob/main/flores-el-olor-analytics-dashboard/images/radargerencial2.png)

---

# Objetivo

El dashboard busca responder preguntas estratégicas como:

- ¿Qué fincas presentan porcentajes de pérdida superiores al promedio?
- ¿Cuáles tienen mayores costos por tallo exportado?
- ¿Existe dependencia comercial de determinados mercados?
- ¿Qué variedades generan pérdidas significativas?
- ¿Existen riesgos de desabastecimiento para 2027?
- ¿Qué operaciones requieren atención inmediata por parte de la gerencia?

---

# Caso de Estudio

Flores El Olor S.A.S. es una empresa ficticia dedicada a la producción y exportación de flores tipo crisantemo.

A partir de información histórica entre los años 2021 y 2026 y proyecciones para 2027, se construyó una arquitectura de análisis basada completamente en servicios de AWS para:

- Centralizar información en un Data Lake.
- Ejecutar consultas SQL analíticas.
- Obtener indicadores de negocio.
- Detectar anomalías operativas.
- Identificar riesgos productivos.
- Visualizar resultados mediante una aplicación web.

---

# Diseño de la Aplicación

La solución fue diseñada siguiendo una arquitectura desacoplada donde almacenamiento, procesamiento y visualización se encuentran separados.

## Amazon S3

Amazon S3 funciona como Data Lake de la solución.

En este servicio se almacenan:

- Información histórica de producción.
- Datos de exportación.
- Costos operativos.
- Información de nómina variable.
- Proyecciones para 2027.

Los datos permanecen almacenados en S3 y son consultados directamente por Athena.

---

## AWS Glue Data Catalog

AWS Glue Catalog administra los metadatos de las tablas externas utilizadas por Athena.

Entre las tablas registradas se encuentran:

- fincas
- variedades
- empleados
- lotes_produccion
- cortes
- empaque
- pedidos
- exportaciones
- exportaciones_curated
- costos
- nomina_variable
- forecast_2027

Estas tablas permiten consultar información utilizando SQL sin necesidad de mover los archivos del Data Lake.

---

## Amazon Athena

Athena constituye la capa analítica de la solución.

Todas las visualizaciones del dashboard son construidas mediante consultas SQL ejecutadas directamente sobre Athena.

Las consultas permiten calcular indicadores relacionados con:

- Producción.
- Pérdidas.
- Costos.
- Mercados internacionales.
- Variedades productivas.
- Proyecciones de demanda.
- Riesgos futuros.

---

## Amazon EC2

La aplicación web fue desplegada en una instancia Amazon EC2 con sistema operativo Linux.

Dentro de la instancia se configuró:

- Python.
- Entorno virtual.
- Streamlit.
- PyAthena.
- Dependencias requeridas por el proyecto.

El dashboard se ejecuta como un servicio administrado mediante systemd para garantizar disponibilidad continua.

---

## Streamlit

Streamlit constituye la capa de presentación.

Sus responsabilidades incluyen:

- Ejecutar consultas sobre Athena.
- Procesar información mediante Pandas.
- Generar indicadores ejecutivos.
- Construir gráficos interactivos con Plotly.
- Publicar la información mediante una interfaz web accesible desde Internet.

---

# Arquitectura Implementada

```text
Usuario
   │
   ▼

URL Pública
http://3.89.204.194:8501

   │
   ▼

Amazon EC2
(Streamlit)

   │
   ▼

Amazon Athena

   │
   ▼

AWS Glue Data Catalog

   │
   ▼

Amazon S3
(Data Lake)
```

---

# Flujo de Datos

Cada vez que un usuario accede a la aplicación se ejecuta el siguiente flujo:

1. El usuario accede a la URL pública.
2. La solicitud llega a la instancia EC2.
3. Streamlit ejecuta consultas SQL sobre Athena.
4. Athena consulta los datos almacenados en Amazon S3.
5. Los resultados son enviados a la aplicación.
6. Pandas procesa la información obtenida.
7. Plotly genera las visualizaciones.
8. El dashboard es renderizado y mostrado al usuario.

Toda la información es obtenida dinámicamente desde Athena en tiempo real.

No se utilizan archivos CSV descargados manualmente ni datos almacenados localmente.

---

# Tecnologías Utilizadas

- Python
- Streamlit
- Pandas
- Plotly
- PyAthena
- Boto3
- Amazon S3
- AWS Glue Data Catalog
- Amazon Athena
- Amazon EC2
- Linux
- Systemd
- GitHub

---

# Estructura del Proyecto

```text
dashboard-flores-el-olor-athena
│
├── app.py
├── consultas.sql
├── requirements.txt
├── README.md
│
└── images
    ├── pikachuflor.gif
    ├── radargerencial.png
    ├── radargerencial2.png
    ├── s3structure.png
    └── athenaConsults.png
```

---

## Aplicación Web Desplegada

La aplicación se encuentra desplegada en una instancia Amazon EC2 y es accesible públicamente mediante la siguiente URL:

### URL pública del Dashboard

```text
http://3.89.204.194:8501
```

La aplicación permanece disponible mientras la instancia EC2 se encuentre encendida.

La solución implementa una arquitectura analítica completa sobre AWS, consumiendo datos directamente desde Amazon Athena y Amazon S3 sin utilizar archivos CSV descargados localmente.

---

# Instalación

## Clonar el repositorio

```bash
git clone https://github.com/mriatorres/dashboard-flores-el-olor-athena.git
```

Ingresar al proyecto:

```bash
cd dashboard-flores-el-olor-athena
```

---

## Crear entorno virtual

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# Dependencias

```txt
streamlit
pandas
plotly
pyathena
boto3
```

---

# Ejecución Local

```bash
streamlit run app.py
```

Acceso local:

```text
http://localhost:8501
```

---

# Despliegue en Amazon EC2

La versión final fue desplegada en una instancia Amazon EC2.

La aplicación se ejecuta mediante:

```bash
streamlit run app.py \
--server.address 0.0.0.0 \
--server.port 8501
```

Posteriormente fue configurada como un servicio persistente utilizando systemd.

Beneficios:

- Arranque automático.
- Reinicio automático ante fallos.
- Disponibilidad permanente.
- Acceso mediante URL pública.

URL de acceso:

```text
http://3.89.204.194:8501
```

---

# Indicadores Ejecutivos

La sección superior del dashboard presenta indicadores diseñados para resumir rápidamente las principales situaciones de interés para la gerencia.

## Mayor Costo por Tallo

Identifica la finca con el mayor costo promedio por tallo exportado.

Fórmula:

```text
Costo Total
/
Tallos Exportados
```

Permite identificar operaciones productivas con costos elevados.

---

## Dependencia Comercial (%)

Representa el porcentaje de ingresos generado por el principal mercado comprador.

Permite evaluar el nivel de concentración comercial y el riesgo asociado a depender de pocos mercados.

---

## Meses en Riesgo

Muestra la cantidad de meses donde:

```text
Demanda Proyectada > Producción Proyectada
```

Permite anticipar posibles escenarios de desabastecimiento.

---

# Visualizaciones

## Producción vs Pérdidas

Gráfico de dispersión que compara:

- Producción exportada.
- Porcentaje de pérdida.
- Cantidad de pérdidas.

Permite detectar fincas con comportamientos operativos atípicos.

---

## Costo por Tallo Exportado

Gráfico de barras utilizado para comparar la eficiencia económica entre fincas.

Permite identificar operaciones con mayores costos productivos.

---

## Variedades Problemáticas

Relaciona pérdidas registradas e ingresos generados por cada variedad.

Facilita la identificación de variedades con bajo retorno económico.

---

## Dependencia Comercial

Visualización tipo Treemap donde cada bloque representa un país comprador.

Permite analizar la distribución geográfica de los ingresos.

---

## Riesgo de Desabastecimiento 2027

Compara:

- Producción proyectada.
- Demanda proyectada.

Permite identificar periodos futuros donde la producción prevista podría resultar insuficiente.

---

# Consultas SQL

Las consultas SQL utilizadas por la aplicación se encuentran documentadas en:

```text
consultas.sql
```

Dichas consultas son ejecutadas dinámicamente sobre Amazon Athena durante la ejecución del dashboard.

---

# Evidencias

## Data Lake en Amazon S3

![](https://github.com/mriatorres/dashboard-flores-el-olor-athena/blob/main/flores-el-olor-analytics-dashboard/images/s3structure.png)

---

## Consultas SQL en Amazon Athena

![](https://github.com/mriatorres/dashboard-flores-el-olor-athena/blob/main/flores-el-olor-analytics-dashboard/images/athenaConsults.png)
---

## Dashboard Analítico

![](https://github.com/mriatorres/dashboard-flores-el-olor-athena/blob/main/flores-el-olor-analytics-dashboard/images/radargerencial2.png)
---

# Hallazgos Esperados

El dashboard permite identificar:

- Fincas con pérdidas superiores al promedio.
- Operaciones con altos costos por tallo exportado.
- Dependencia de mercados específicos.
- Variedades con bajo rendimiento económico.
- Riesgos de desabastecimiento para 2027.

---

# Cumplimiento Académico

La solución implementa una arquitectura analítica completa basada en servicios de AWS.

El proyecto integra:

- Amazon S3 como Data Lake.
- AWS Glue Data Catalog para metadatos.
- Amazon Athena para procesamiento analítico mediante SQL.
- Amazon EC2 para despliegue de la aplicación.
- Streamlit como capa de visualización.
- URL pública para acceso remoto.

Toda la información presentada en el dashboard es obtenida dinámicamente desde Amazon Athena durante la ejecución de la aplicación.

---

# Conclusión

El Radar Gerencial de Anomalías transforma información almacenada en un Data Lake de AWS en conocimiento útil para la toma de decisiones.

La integración entre Amazon S3, AWS Glue Data Catalog, Amazon Athena, Amazon EC2 y Streamlit permite construir una solución analítica capaz de detectar:

- Ineficiencias operativas.
- Pérdidas productivas.
- Dependencia comercial.
- Problemas asociados a determinadas variedades.
- Riesgos futuros de abastecimiento.

La aplicación constituye una capa de visualización construida sobre una arquitectura moderna de analítica de datos en la nube.

---

# Autor

**María Fernanda Toro Torres**

Ingeniería en Inteligencia Artificial y Ciencia de Datos

Universidad Pontificia Bolivariana

2026
