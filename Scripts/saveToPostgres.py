import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook

def save_to_postgres(**context):
    df = pd.DataFrame(context['ti'].xcom_pull(task_ids='fetch_latest_albums'))
    postgres_hook = PostgresHook(postgres_conn_id='postgres_default')
    engine = postgres_hook.get_sqlalchemy_engine()
    df.to_sql('latest_albums', engine, if_exists='replace', index=False)
