from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

# Import task functions
from scripts.fetch_latest_albums import fetch_latest_albums
from scripts.save_to_postgres import save_to_postgres
from scripts.fetch_from_postgres import fetch_from_postgres
from scripts.collect_additional_data import collect_additional_data

default_args = {
    'owner': 'airflow',
    'retries': 1,
}

with DAG(
    dag_id='spotify_to_postgres_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
) as dag:

    fetch_data_task = PythonOperator(
        task_id='fetch_latest_albums',
        python_callable=fetch_latest_albums
    )

    save_to_db_task = PythonOperator(
        task_id='save_to_postgres',
        python_callable=save_to_postgres
    )

    process_data_task = PythonOperator(
        task_id='fetch_from_postgres',
        python_callable=fetch_from_postgres
    )

    collect_more_data_task = PythonOperator(
        task_id='collect_additional_data',
        python_callable=collect_additional_data
    )

    fetch_data_task >> save_to_db_task >> process_data_task >> collect_more_data_task
