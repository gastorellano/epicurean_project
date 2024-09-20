from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from google.cloud import storage
import googlemaps
from datetime import datetime, timedelta
import logging
import json

# Define tus variables
API_KEY = 'AIzaSyB6cB_lSeOllIwjeFbPipt'  # Reemplaza esto con tu API Key de Google Places
BUCKET_NAME = 'us-central1-epicureanairflo-06d3607-bucket'  # Reemplaza con tu bucket de GCS
PLACE_ID = 'ChIJN1t_tDeuEmsRUsoyG83frY4'  # Reemplaza con el Place ID del lugar que quieres obtener reseñas

# Argumentos por defecto para el DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 9, 19),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Definir el DAG
dag = DAG(
    'google_api_etl',
    default_args=default_args,
    description='DAG para obtener reseñas de Google y guardarlas en GCS',
    schedule_interval='@daily',  # Puedes ajustar el intervalo según necesites
    catchup=False
)


# Función para obtener reseñas desde la API de Google
def fetch_google_reviews(**kwargs):
    gmaps = googlemaps.Client(key=API_KEY)
    try:
        # Obtener detalles del lugar, incluyendo reseñas
        place_details = gmaps.place(place_id=PLACE_ID, fields=['name', 'rating', 'review'])
        reviews = place_details.get('result', {}).get('reviews', [])

        # Guardar el resultado en XCom para la siguiente tarea
        kwargs['ti'].xcom_push(key='google_reviews', value=reviews)
        logging.info(f"Se obtuvieron {len(reviews)} reseñas del lugar.")
    except Exception as e:
        logging.error(f"Error al obtener reseñas: {e}")
        raise


# Función para guardar reseñas en GCS
def save_reviews_to_gcs(**kwargs):
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)

    # Recuperar reseñas desde XCom
    reviews = kwargs['ti'].xcom_pull(key='google_reviews', task_ids='fetch_reviews')
    if not reviews:
        raise ValueError("No se encontraron reseñas para guardar.")

    # Guardar reseñas en formato JSON
    reviews_blob = bucket.blob('data/google_reviews.json')
    reviews_blob.upload_from_string(json.dumps(reviews), content_type='application/json')
    logging.info("Las reseñas se guardaron en GCS con éxito.")


# Tareas del DAG
fetch_reviews_task = PythonOperator(
    task_id='fetch_reviews',
    python_callable=fetch_google_reviews,
    provide_context=True,
    dag=dag,
)

save_reviews_task = PythonOperator(
    task_id='save_reviews',
    python_callable=save_reviews_to_gcs,
    provide_context=True,
    dag=dag,
)

# Definir la secuencia de ejecución de las tareas
fetch_reviews_task >> save_reviews_task
