from airflow import DAG
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.utils.dates import datetime

# Definir el DAG con argumentos por defecto
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Crear el DAG
dag = DAG(
    'upload_parquet_to_bigquery',
    default_args=default_args,
    description='Sube archivo Parquet desde GCS a BigQuery',
    schedule_interval=None,  # Sin programación automática
    start_date=datetime(2024, 9, 17),  # Fecha de inicio actual
)

# Tarea para cargar el archivo Parquet a BigQuery y crear la tabla si no existe
load_parquet_to_bq = GCSToBigQueryOperator(
    task_id='load_parquet_to_bq',
    bucket='us-central1-epicureandag-3b408e2a-bucket',  # Nombre del bucket
    source_objects=['data/estado/reviews-California.parquet'],  # Ruta del archivo en el bucket
    destination_project_dataset_table='epicurean-project.epicurean_dataset.state',  # Reemplazar con el dataset/tabla de BigQuery
    source_format='PARQUET',
    write_disposition='WRITE_TRUNCATE',  # Sobrescribe la tabla si existe
    create_disposition='CREATE_IF_NEEDED',  # Crea la tabla si no existe
    dag=dag,
)

load_parquet_to_bq
