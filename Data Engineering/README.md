# Ingeniería de Datos: ETL, Estructura implementada y automatización


<p align="center">
  <img src="/IMG/ingenieria-datos.jpg" alt="ingenieria" />
</p>

A continuación se realizará una explicación detallada de los procedimientos desarrollados. Puedes visualizar el funcionamiento en [este video](https://www.youtube.com/watch?v=8_UMW77SLqo).

## Descripción General
En esta etapa se promovió la creación de un **Data Warehouse** (DW) automatizado utilizando Google Cloud Platform (GCP), Google Storage, Google BigQuery y Apache Airflow para la automatización del pipeline ETL. La estructura de datos implementada permite la carga, transformación y análisis de grandes volúmenes de datos de forma eficiente y escalable. Se ha trabajado en la construcción de pipelines para la ingesta de datos hacia el **Data Warehouse**, así como en la validación y automatización del proceso ETL.

## Tecnologías Utilizadas
- **Google Cloud Platform (GCP):** Infraestructura en la nube utilizada para alojar y gestionar el **Data Warehouse** y el **Data Lake**.
- **Google Storage:** Servicio de almacenamiento utilizado como punto de entrada para los datos en bruto.
- **Google BigQuery:** Herramienta de almacenamiento y análisis de datos utilizada como **Data Warehouse**.
- **Apache Airflow:** Plataforma de automatización utilizada para crear y gestionar los pipelines ETL, mediante la creación de DAGs (Directed Acyclic Graphs).
- **APIs de GCP:** Configuración de APIs para gestionar la integración entre Google Storage y Google BigQuery.
- **APIs de Google Maps:** En particular, se ha establecido una conexión para asegurar la carga incremental de registros.

<p align="center">
  <img src="/IMG/tecnologias-ingenieria.jpeg" alt="tecnologias" />
</p>

## Procesos cumplimentados:

### 1. ETL Completo
A partir de las muestras correspondientes, se desarrolló un código localmente con Python y galerías como Pandas y Numpy, que permitió establecer el proceso de extracción, transformación y carga (ETL). Ello fue el puntapié inicial para avanzar con datos ya depurados, y sirvió de base para automatizar el proceso con volúmenes de datos más grandes, como los que se utilizan en el presente proyecto.
Este proceso se ha integrado con Google Cloud Storage para la ingesta de archivos y Google BigQuery para el almacenamiento de los datos procesados.

### 2. Estructura de Datos Implementada
Se ha diseñado una arquitectura de datos que incluye un **Data Lake** en **Google Cloud Storage** y un **Data Warehouse** en **Google BigQuery**. Esta estructura permite manejar tanto los datos en crudo como los datos procesados, facilitando la transformación y el análisis.

### 3. Pipeline ETL Automatizado
El pipeline ETL ha sido automatizado utilizando **Apache Airflow**. Se han definido **DAGs** para gestionar el flujo de trabajo del ETL, asegurando que los datos cargados en Google Cloud Storage sean transformados y posteriormente cargados en BigQuery. Los DAGs permiten ejecutar el proceso de manera recurrente y monitoreada, optimizando la eficiencia del flujo de datos.

### 4. Diseño del Modelo ER
Se ha creado un **Modelo Entidad-Relación (ER)** que define las relaciones entre las distintas tablas en el **Data Warehouse**. Este modelo asegura que los datos se organicen de manera eficiente y facilita la realización de consultas complejas en BigQuery.

La Base de Datos se encuentra implementada con tres tablas base:
- Business:
Tiene los siguientes atributos: gmap_id (PRIMARY KEY), name, address, latitude, longitude, category, avg_rating, num_of_reviews, relative_results, service_options, clasificacion, address_depurada, city, county.
- Reviews:
Tiene las siguientes columnas: review_id (PRIMARY KEY), gmap_id (Foreign Key), user_id, name, time, rating, text.
- Ubicaciones:
Tiene las siguientes columnas: id_locacion (PRIMARY KEY), gmap_id (Foreign Key), address_depurada, city, county, latitude, longitude.

<p align="center">
  <img src="/IMG/DER/DER.jpeg" alt="DER" />
</p>

La Tabla Business tiene una relación 1 a N con la tabla Reviews, a través de la clave 'gmap_id'. A su vez, la tabla Business tiene una relación 1 a 1 con la tabla Ubicaciones, también sobre la clave 'gmap_id'.

Esa es la Base de Datos implementada en el servicio Google Cloud.
A la hora de realizar preliminarmente el Dashboard, se incorpora la tabla 'análisis_económico', con las siguientes columnas: County (PRIMARY KEY), Per capita income, Rent y Property Cost.
Esta tabla se encuentra conectada en una relación 1 a 1 con la tabla Ubicaciones, a través de su columna 'county'. De esa forma, se puede implementar el Dashboard relacionando correctamente los datos.

<p align="center">
  <img src="/IMG/DER/DER_final.jpeg" alt="DER Dashboards" />
</p>

**En este esquema se pueden visualizar los tipos de datos**


### 5. Pipelines para Alimentar el Data Warehouse
Los pipelines han sido configurados para realizar la extracción de datos desde el **Data Lake** (Google Cloud Storage), procesar estos datos mediante scripts de transformación, y cargarlos en las tablas correspondientes del **Data Warehouse** (Google BigQuery). Este proceso garantiza que los datos almacenados en el DW estén limpios y listos para análisis.

### 6. Data Warehouse
El **Data Warehouse** está alojado en **Google BigQuery**, donde se almacenan los datos procesados tras el pipeline ETL. La arquitectura diseñada permite consultas rápidas y eficientes para análisis y reportes, aprovechando la escalabilidad y el poder de procesamiento de BigQuery.

### 7. Automatización
La automatización se ha implementado utilizando **Apache Airflow**. Los DAGs definidos en Airflow permiten que los pipelines ETL se ejecuten de manera periódica o según eventos específicos, eliminando la necesidad de intervenciones manuales. Esto asegura la consistencia y la integridad de los datos a lo largo del tiempo.

### 8. Carga Incremental
Se ha establecido una conexión con la **API de Google Maps** para realizar una carga incremental de los registros del **Data Warehouse**, a través de un DAG programado en **Airflow**.

### 9. Validación de Datos
Se han implementado pasos de validación de datos dentro del pipeline ETL. Esto incluye la verificación de formatos y la consistencia de los datos antes de ser cargados al **Data Warehouse**, garantizando la calidad de la información almacenada.

### 10. Diccionario de Datos:
Puede ser de utilidad el diccionario de los datos utilizados, a partir de las tablas y datasets.
Se puede acceder a los mismos [aquí](https://docs.google.com/document/d/12K4dz8ffNsChKgihCfpXEN-vhH1fH6C1vZFpXCwZwhs/edit?usp=sharing).



# Workflow de Tecnologías Utilizadas
El siguiente es un flujo detallado del proceso implementado y las tecnologías involucradas:

1. **Ingesta de Datos**:
   - Los datos en crudo son almacenados en **Google Cloud Storage**.
   - Archivos CSV y otros formatos se cargan manual o automáticamente en el **Data Lake**.
   - Se realiza una conexión a la **API de Google Maps** para obtener datos geoespaciales adicionales. Estos datos se utilizan para enriquecer la información existente y son cargados de forma incremental al **Data Warehouse** mediante un proceso programado en **Apache Airflow**.

2. **Transformación de Datos (ETL)**:
   - Se utiliza un pipeline ETL desarrollado a partir del código dispuesto para transformar los datos en crudo. Dicho código, que se utilizó primigeniamente para un proceso de ETL sobre una muestra reducida, puede visualizarse [aquí](/Data%20Engineering/ETL/ETL_Google).
   - Las transformaciones incluyen limpieza, normalización y enriquecimiento de los datos.

3. **Carga de Datos**:
   - Los datos procesados son cargados en **Google BigQuery**, donde se almacenan en tablas optimizadas para consultas y análisis.

4. **Automatización**:
   - **Apache Airflow** se utiliza para automatizar el pipeline ETL, definiendo flujos de trabajo a través de DAGs que se ejecutan según cronogramas o eventos.

5. **Consulta y Análisis**:
   - Los datos almacenados en el **Data Warehouse** son accesibles mediante **Google BigQuery**, permitiendo la realización de consultas SQL y análisis complejos.

## Futuras Implementaciones
- Implementar dashboards y reportes sobre los datos almacenados en el **Data Warehouse** utilizando herramientas como **Google Data Studio**, **Tableau** o **Power BI**.