## Análisis rubro gastronómico en California de Estados Unidos
Ingeniería de Datos en la Nube con Airflow y Google Cloud Platform

<p align="center">
  <img src="/IMG/logo_epicurean.jpeg" alt="Logo" />
</p>

## Indice

<details>
  <summary>Tabla de contenido</summary>

  1. [Índice](#indice)
  2. [Presentación](#presentación)
  3. [Propuesta de Proyecto](#propuesta-de-proyecto)
  4. [Arquitectura del proyecto](#stack-tecnológico)
  5. [Ciclo de Vida del Dato](#ciclo-de-vida-del-dato)
  6. [Configuración del Entorno](#análisis-exploratorio)
  7. [Diagrama Entidad-Relación](#análisis-exploratorio)
  8.[Conclusión](#análisis-exploratorio)

</details>

## Presentación

Este README documenta el proceso de configuración del Data Warehouse en BigQuery y la creación de las tablas base para
el proyecto _Epicurean Project_. Estas tablas almacenarán los datos procesados desde Google Cloud Storage y serán 
utilizadas para el análisis y la generación de insights en el sistema de recomendaciones.

Nuestro enfoque se centra en la optimización de procesos, la identificación de oportunidades de crecimiento y la mejora 
de la eficiencia operativa en el sector gastronómico, todo basado en datos precisos y estrategias bien fundamentadas.
En EPICUREAN estamos comprometidos con acompañar a las empresas en su transformación digital, brindándoles insights 
valiosos que impulsen su éxito en un mercado competitivo.

## Propuesta de Proyecto

El objetivo de este proyecto es realizar un análisis exhaustivo del sector gastronómico en California, en zonas tech 
Estados Unidos, utilizando datos extraídos de la API de Google Places. El proyecto se llevará a cabo en Google Cloud 
Platform (GCP), utilizando Apache Airflow para orquestar y automatizar el pipeline de datos, desde la extracción hasta 
el almacenamiento y análisis en BigQuery.

Los resultados finales permitirán a los stakeholders tomar decisiones informadas sobre inversiones, tendencias de 
mercado y comportamiento del consumidor en el sector gastronómico.


## Arquitectura del Proyecto

*Apache Airflow: Se utiliza como orquestador de tareas para programar y ejecutar flujos de trabajo de datos.
*Google Cloud Storage (GCS): Almacena los archivos de datos en diferentes etapas del proceso ETL.
*BigQuery: Almacena los datos transformados para realizar análisis y consultas a gran escala.
*API de Google Places: Fuente de datos que contiene información sobre establecimientos en California de Estados Unidos.

# Ciclo de Vida de los Datos en la Nube

1. Extracción de Datos
Se utiliza Airflow para orquestar la extracción de datos desde la API de Google Reviews. Los datos se recuperan en 
formato JSON y se almacenan temporalmente en Google Cloud Storage (GCS).
2. Creación de dats base 
3. Almacenamiento Inicial en Google Cloud Storage
Los datos extraídos se almacenan en un bucket de GCS en formato crudo, dentro de una estructura de carpetas organizada 
por fecha y tipo de datos. Esto permite una fácil recuperación y gestión de versiones. 
4. Transformación de Datos
Se utilizan scripts de Python dentro de Airflow para transformar los datos crudos. Esto incluye:
Limpieza de datos. 
5. Normalización y estructuración.
Conversión a formatos optimizados como Parquet.
Los datos transformados se guardan en una subcarpeta de GCS.
6. Carga de Datos en BigQuery
Airflow se encarga de cargar los datos transformados desde GCS a BigQuery. Se crean tablas particionadas y optimizadas 
para realizar consultas eficientes. En BigQuery se realizan operaciones de modelado de datos para preparar los datos 
para su análisis. 
7. Análisis y Visualización
Con los datos en BigQuery, se pueden crear dashboards interactivos utilizando herramientas como Google Data Studio o 
realizar análisis avanzados con SQL. 
8. Monitoreo y Mantenimiento
Airflow ejecuta flujos de trabajo de manera periódica. Se configuran alertas para detectar errores en el pipeline y se 
realiza mantenimiento de los datos almacenados en GCS y BigQuery.

# Configuración del Entorno

1. Instalación de Dependencias
apache-airflow: Orquestador de flujos de trabajo.
google-cloud-storage: Cliente para interactuar con GCS.
google-cloud-bigquery: Cliente para interactuar con BigQuery.
googlemaps: Cliente para interactuar con la API de Google Reviews.

<p align="center">
  <img src="/IMG/estado_california.jpeg" alt="California" />
</p>

2. Configuración de Airflow

Configura las conexiones y variables necesarias en la interfaz de Airflow:
  Google Cloud Storage Connection: Configura una conexión con las credenciales adecuadas para acceder a GCS.
  Google BigQuery Connection: Configura una conexión con las credenciales adecuadas para acceder a BigQuery.

3. Ejecución de los DAGs

Para iniciar el pipeline de datos, activa y ejecuta los DAGs en la interfaz de Airflow.
Monitorea el estado de las tareas y revisa los logs para detectar y solucionar problemas.

# Diagrama Entidad-Relación

La Base de Datos se encuentra implementada con tres tablas:

- **reviews**
  - `review_id: STRING`
  - `gmap_id: STRING`
  - `name: STRING`
  - `text: STRING`
  - `time: DATE`
  - `rating: FLOAT`

- **business**
  - `gmap_id: STRING`
  - `adress: STRING`
  - `adress_depurada: STRING`
  - `category: STRING`
  - `avg_rating: FLOAT`
  - `county: STRING`
  - `clasificación`
  - `latitude: FLOAT`
  - `longitude: FLOAT`

- **epicurean_yelp**
  - `gmap_id: FLOAT`
  - `adress_depurada: STRING`
  - `latitude: FLOAT`
  - `longitude: FLOAT`
  - `id_locación: STRING`
  - `city: STRING`
  - `county: STRING`

<p align="center">
  <img src="/IMG/ER_diagram.png" alt="ER" />


# Conclusión

Este proyecto demuestra cómo utilizar Airflow y Google Cloud para construir un pipeline de datos robusto y escalable en
la nube. La flexibilidad y escalabilidad de estas herramientas permite manejar grandes volúmenes de datos de manera 
eficiente, con la posibilidad de extender el flujo de trabajo según las necesidades del proyecto.