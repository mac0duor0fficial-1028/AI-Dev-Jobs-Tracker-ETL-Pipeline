from datetime import datetime, timedelta
import pandas as pd

from airflow import DAG
from airflow.operators import PythonOperator

from src.extract import extract_jobs
from src.transform import transform_jobs
from src.load import load_jobs_to_postgres

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 11, 1),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

def extract_wrapper(**kwargs):
    return extract_jobs()

def transform_wrapper(**kwargs):
    ti = kwargs['ti']
    raw_data = ti.xcom_pull(task_ids='extract_data')
    cleaned_df = transform_jobs(raw_data)
    # Transit clean dataframe structure as serialized JSON string stream via XCom
    return cleaned_df.to_json(orient='records')

def load_wrapper(**kwargs):
    ti = kwargs['ti']
    transformed_json = ti.xcom_pull(task_ids='transform_data')
    cleaned_df = pd.read_json(transformed_json, orient='records')
    load_jobs_to_postgres(cleaned_df)

with DAG(
    dag_id='ai_jobs_etl_pipeline',
    default_args=default_args,
    description='Automated production pipeline collecting data insights for AI Dev workflows',
    schedule_interval='@daily',
    catchup=False,
    max_active_runs=1,
) as dag:

    extract_data = PythonOperator(
        task_id='extract_data',
        python_callable=extract_wrapper,
    )

    transform_data = PythonOperator(
        task_id='transform_data',
        python_callable=transform_wrapper,
    )

    load_data = PythonOperator(
        task_id='load_data',
        python_callable=load_wrapper,
    )

    extract_data >> transform_data >> load_data
