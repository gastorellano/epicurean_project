## Proyecto Análisis rubro gastronómico en principales polos de Estados 

# Epicurean Project - Configuración del Data Warehouse y Tablas Base

## Descripción
Este README documenta el proceso de configuración del Data Warehouse en BigQuery y la creación de las tablas base para el proyecto _Epicurean Project_. Estas tablas almacenarán los datos procesados desde Google Cloud Storage y serán utilizadas para el análisis y la generación de insights en el sistema de recomendaciones.

## Estructura del Proyecto
El proyecto está organizado en un dataset de BigQuery llamado `epicurean_dataset`, el cual contiene las siguientes tablas:
1. **epicurean_reviews**: Tabla que contiene reseñas de los negocios.
2. **epicurean_business**: Información básica de los negocios.
3. **epicurean_maps**: Información de los negocios obtenida de Google Maps.
4. **epicurean_yelp**: Información de los negocios obtenida de Yelp.

Los datos serán cargados desde archivos `.parquet` almacenados en Google Cloud Storage y procesados a través de pipelines automatizados.

## Configuración

### 1. Creación del Dataset
- El dataset `epicurean_dataset` fue creado en BigQuery para almacenar todas las tablas del proyecto.
- Ubicación: US (multiregión).

### 2. Creación de Tablas Base
Se crearon las siguientes tablas con sus respectivos esquemas:

- **epicurean_reviews**
  - `review_id: STRING`
  - `user_id: STRING`
  - `platform_id: STRING`
  - `business_id: STRING`
  - `text: STRING`
  - `date: DATE`
  - `rating: FLOAT`

- **epicurean_business**
  - `business_id: STRING`
  - `name: STRING`
  - `latitude: FLOAT`
  - `longitude: FLOAT`

- **epicurean_maps**
  - `gmap_id: STRING`
  - `name: STRING`
  - `category_id: STRING`
  - `business_category: STRING`
  - `latitude: FLOAT`
  - `longitude: FLOAT`
  - `address: STRING`
  - `avg_rating: FLOAT`
  - `num_of_reviews: INTEGER`
  - `hours: STRING`
  - `attributes: STRING`
  - `business_id: STRING`

- **epicurean_yelp**
  - `yelp_id: STRING`
  - `name: STRING`
  - `category_id: STRING`
  - `business_category: STRING`
  - `latitude: FLOAT`
  - `longitude: FLOAT`
  - `address: STRING`
  - `avg_rating: FLOAT`
  - `num_of_reviews: INTEGER`
  - `hours: STRING`
  - `attributes: STRING`
  - `business_id: STRING`

### 3. Configuración de Credenciales y Claves JSON
- Se activó el servicio de Google Cloud para la autenticación mediante claves JSON.
- Se generaron cuentas de servicio específicas para cada integrante del equipo y se proporcionaron los archivos JSON correspondientes para cada uno.

Las cuentas de servicio generadas incluyen:

- **Analía (Ingeniera 1)**: Encargada de la configuración del ETL y la gestión de datos.
- **Yesica (Ingeniera 2)**: Encargada de la automatización del pipeline ETL y la carga de datos en BigQuery y Google Cloud Storage.
- **Gaston (Ingeniero de análisis de datos)**: Encargado del análisis de datos en BigQuery.
- **Melanie (Ingeniera de recomendaciones)**: Responsable del sistema de recomendaciones basado en análisis de reseñas.

Cada miembro tiene una clave JSON asignada, la cual se puede usar para autenticarse en el sistema y ejecutar procesos en Google Cloud.

### 4. Automatización del Pipeline
Yesica será responsable de la automatización del pipeline usando Airflow o Composer para cargar los archivos `.parquet` en las tablas correspondientes de BigQuery. El pipeline estará configurado para ejecutar cargas incrementales y programadas.

### 5. Próximos Pasos
- Yesica se encargará de iniciar el pipeline automatizado en Airflow.
- Analía verificará la integridad de las tablas y el flujo de datos.
- Gaston y Melanie comenzarán a trabajar en el análisis y las recomendaciones una vez los datos estén cargados.

## Contacto
Para cualquier duda o actualización, contactar a:
- **Analía (Ingeniera 1)**: Encargada del Data Warehouse y creación de tablas base.
- **Yesica (Ingeniera 2)**: Encargada de la automatización del pipeline y la carga de datos.
