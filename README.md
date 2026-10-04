# Radar Gerencial de Anomalías ![](https://github.com/mriatorres/dashboard-flores-el-olor-athena/blob/main/flores-el-olor-analytics-dashboard/images/pikachuflor.gif)



## Flores El Olor S.A.S. 

Dashboard analítico desarrollado como evidencia complementaria para el examen práctico de Arquitecturas de Nube y Big Data.

La aplicación transforma resultados obtenidos mediante consultas SQL ejecutadas sobre Amazon Athena en visualizaciones interactivas orientadas a apoyar la toma de decisiones dentro del caso empresarial de Flores El Olor S.A.S.

El enfoque del análisis está centrado en la identificación de patrones, anomalías operativas, riesgos productivos y oportunidades de mejora que podrían requerir atención gerencial.

![](https://github.com/mriatorres/dashboard-flores-el-olor-athena/blob/main/flores-el-olor-analytics-dashboard/images/radargerencial.png)

![](https://github.com/mriatorres/dashboard-flores-el-olor-athena/blob/main/flores-el-olor-analytics-dashboard/images/radargerencial2.png)

---

# Objetivo

El dashboard busca responder preguntas como:

- ¿Qué fincas presentan porcentajes de pérdida superiores al promedio?
- ¿Cuáles tienen mayores costos por tallo exportado?
- ¿Existe dependencia comercial de determinados mercados?
- ¿Qué variedades generan pérdidas importantes?
- ¿Existen riesgos de desabastecimiento en las proyecciones para 2027?
- ¿Qué situaciones deberían ser revisadas por la gerencia?

---

# Caso de Estudio

Flores El Olor S.A.S. es una empresa ficticia dedicada a la producción y exportación de crisantemos.

A partir de información histórica entre 2021 y 2026 y proyecciones para 2027, se construyó una arquitectura de análisis utilizando servicios de AWS para:

- Almacenar información.
- Organizar datos en un Data Lake.
- Crear tablas externas.
- Ejecutar consultas SQL.
- Obtener indicadores de negocio.

Posteriormente se desarrolló este dashboard como mecanismo de visualización de resultados.

---

# Arquitectura Utilizada

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

# Flujo de Datos

Las visualizaciones mostradas en la aplicación provienen de consultas ejecutadas en Amazon Athena.

Proceso utilizado:

1. Carga de archivos al bucket S3.
2. Creación de tablas externas en Athena.
3. Ejecución de consultas SQL analíticas.
4. Exportación de resultados desde Athena.
5. Descarga de resultados en formato CSV.
6. Consumo de dichos resultados desde Streamlit.
7. Generación de visualizaciones interactivas.

---

# Tecnologías Utilizadas

- Python
- Streamlit
- Pandas
- Plotly
- Amazon S3
- AWS Glue Catalog
- Amazon Athena
- GitHub

---

# Estructura del Proyecto

```text
flores-el-olor-analytics-dashboard
│
├── app.py
├── consultas.sql
├── requirements.txt
├── README.md
├── .gitignore
│
├── data
│   ├── produccion_perdidas.csv
│   ├── costos_por_tallo.csv
│   ├── dependencia_comercial.csv
│   ├── variedades_problematicas.csv
│   └── riesgo_2027.csv
│
└── images
    ├── arquitectura.png
    ├── athena-query.png
    ├── s3-results.png
    ├── dashboard.png
    └── pikachuflor.gif
```

---

# Modelo de Datos Utilizado

Tablas analizadas en Athena:

- fincas
- variedades
- empleados
- lotes_produccion
- cortes
- empaque
- pedidos
- exportaciones
- costos
- nomina_variable
- forecast_2027

Estas tablas fueron utilizadas para generar las consultas SQL que alimentan los archivos CSV consumidos por el dashboard.

---

# Instalación

## 1. Clonar el repositorio

```bash
git clone https://github.com/mriatorres/dashboard-flores-el-olor-athena.git
```

Ingresar al proyecto:

```bash
cd dashboard-flores-el-olor-athena/flores-el-olor-analytics-dashboard
```

---

## 2. Crear entorno virtual (Opcional)

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

---

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 4. Verificar los archivos de datos

La carpeta `data` debe contener:

```text
produccion_perdidas.csv
costos_por_tallo.csv
dependencia_comercial.csv
variedades_problematicas.csv
riesgo_2027.csv
```

Estos archivos corresponden a resultados exportados previamente desde Amazon Athena.

---

# Ejecución

Desde la carpeta principal del proyecto:

```bash
streamlit run app.py
```

La aplicación estará disponible en:

```text
http://localhost:8501
```

---

# Dependencias

Contenido del archivo `requirements.txt`:

```txt
streamlit
pandas
plotly
```

---

# Indicadores Ejecutivos

La primera sección del dashboard presenta indicadores diseñados para resumir rápidamente las principales situaciones de interés para la gerencia.

## Mayor Costo por Tallo

Este indicador identifica la finca con el mayor costo promedio por tallo exportado.

Fórmula:

```text
Costo Total Registrado
/
Tallos Exportados
```

Interpretación:

- Valores bajos indican mayor eficiencia productiva.
- Valores altos sugieren operaciones costosas que podrían afectar la rentabilidad.

Pregunta de negocio:

> ¿Qué finca tiene actualmente el proceso productivo más costoso?

---

## Dependencia Comercial (%)

Representa el porcentaje de ingresos generado por el principal país comprador.

Interpretación:

- Valores altos indican una fuerte dependencia de pocos mercados.
- Valores bajos indican una cartera comercial más diversificada.

Pregunta de negocio:

> ¿Qué tan dependiente es la empresa de un único mercado internacional?

---

## Meses en Riesgo

Indica la cantidad de meses donde la demanda proyectada es superior a la producción proyectada.

Interpretación:

- Valores altos representan escenarios potenciales de desabastecimiento.
- Valores bajos indican una capacidad productiva alineada con la demanda esperada.

Pregunta de negocio:

> ¿Cuántos meses presentan riesgo de incumplimiento en 2027?

---

# Explicación de las Visualizaciones

## Producción vs Pérdidas

Gráfico de dispersión donde cada punto representa una finca.

Variables:

- Eje X: Porcentaje de pérdida.
- Eje Y: Tallos exportados.
- Tamaño del punto: Cantidad total de pérdidas.
- Color: Finca.

Objetivo:

Comparar productividad y pérdidas simultáneamente.

Permite detectar:

- Fincas con pérdidas elevadas.
- Fincas con baja eficiencia operativa.
- Diferencias significativas entre unidades productivas.

---

## Costo por Tallo Exportado

Gráfico de barras que compara el costo promedio por tallo exportado entre fincas.

Objetivo:

Evaluar la eficiencia económica de cada operación productiva.

Permite detectar:

- Fincas con mayores costos.
- Oportunidades de reducción de gastos.
- Desempeños operativos atípicos.

---

## Variedades Problemáticas

Gráfico de dispersión que relaciona pérdidas registradas e ingresos generados por variedad.

Variables:

- Eje X: Pérdidas.
- Eje Y: Ingresos generados.

Objetivo:

Analizar qué variedades aportan menos valor económico frente a las pérdidas asociadas.

Permite detectar:

- Variedades poco rentables.
- Material vegetal con problemas productivos.
- Posibles oportunidades de optimización.

---

## Dependencia Comercial

Visualización tipo Treemap donde cada bloque representa un país comprador.

El tamaño de cada bloque depende del valor facturado.

Objetivo:

Visualizar la distribución geográfica de los ingresos.

Permite detectar:

- Mercados estratégicos.
- Concentración comercial.
- Riesgos asociados a la dependencia de determinados clientes internacionales.

---

## Riesgo de Desabastecimiento 2027

Gráfico temporal que compara:

- Producción proyectada.
- Demanda proyectada.

Objetivo:

Identificar periodos futuros donde la capacidad productiva podría ser insuficiente.

Permite detectar:

- Déficits de producción.
- Riesgos de incumplimiento.
- Necesidades futuras de planeación.

---

## Tabla de Riesgos

Presenta únicamente los periodos donde:

```text
Demanda Proyectada > Producción Proyectada
```

Objetivo:

Mostrar de forma explícita los escenarios que requieren atención inmediata.

Cada fila representa una posible situación de desabastecimiento que podría afectar el cumplimiento de compromisos comerciales.

---

# Consultas SQL

Las consultas utilizadas para generar los archivos CSV se encuentran documentadas en:

```text
consultas.sql
```

Estas consultas fueron ejecutadas sobre Amazon Athena utilizando los datos almacenados en Amazon S3.

---

# Evidencias

## Arquitectura AWS


![](https://github.com/mriatorres/dashboard-flores-el-olor-athena/blob/main/flores-el-olor-analytics-dashboard/images/s3structure.png)

---

## Amazon Athena

![](https://github.com/mriatorres/dashboard-flores-el-olor-athena/blob/main/flores-el-olor-analytics-dashboard/images/athenaConsults.png)

---

## Dashboard

![](https://github.com/mriatorres/dashboard-flores-el-olor-athena/blob/main/flores-el-olor-analytics-dashboard/images/radargerencial2.png)

---

# Hallazgos Esperados

El dashboard permite identificar:

- Fincas con pérdidas superiores al promedio.
- Operaciones productivas con costos elevados.
- Dependencia comercial de mercados específicos.
- Variedades con bajo rendimiento económico.
- Meses donde la demanda proyectada supera la producción prevista.

---

# Cumplimiento Académico

La información utilizada en este dashboard proviene de consultas ejecutadas sobre Amazon Athena utilizando los datos almacenados en Amazon S3.

La aplicación constituye una capa de visualización construida sobre los resultados analíticos obtenidos durante el desarrollo de la arquitectura propuesta para el examen.

---

# Conclusión

El Radar Gerencial de Anomalías transforma resultados analíticos obtenidos mediante Athena en información visual de fácil interpretación.

La solución permite detectar:

- Ineficiencias operativas.
- Pérdidas productivas.
- Riesgos comerciales.
- Problemas asociados a determinadas variedades.
- Riesgos futuros de abastecimiento.

De esta manera, el dashboard convierte información técnica del Data Lake en conocimiento útil para apoyar la toma de decisiones estratégicas dentro de Flores El Olor S.A.S.

---

# Autor

María Fernanda Toro Torres

Ingeniería en Inteligencia Artificial y Ciencia de Datos

Universidad Pontificia Bolivariana

2026
