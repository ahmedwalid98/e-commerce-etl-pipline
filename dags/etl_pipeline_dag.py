import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
from etl.extract_and_transform import (
    extract_customer_data,
    extract_product_data,
    extract_order_data,
    extract_order_items_data,
    extract_seller_data,
    dim_date,
    extract_fact_sales,
)
from etl.load import load_to_dwh

default_args = {
  'owner': 'walid',
  'start_date': days_ago(3),
  'retries': 1,
  'retry_delay': timedelta(minutes=5)
}

with DAG(
  dag_id='etl_pipeline',
  default_args=default_args,
  schedule_interval='@daily'
) as etl_dag:
  create__stage_tables=PostgresOperator(
    task_id='create_the_stage_tables',
    postgres_conn_id='e_commerce_db_conn',
    sql='DDL/DDL_script.sql'
  )
  extract_data_from_csv_to_staging = BashOperator(
    task_id='extract_data_from_csv_to_staging',
    bash_command='python /home/ahmed-walid/e-commerce-etl-pipline/satging_layer/extract_and_stage_data.py'
  )

  load_dim_customer = PythonOperator(
    task_id='load_dim_customer',
    python_callable=lambda: load_to_dwh(extract_customer_data(), 'dim_customer')
  )

  load_dim_product = PythonOperator(
    task_id='load_dim_product',
    python_callable=lambda: load_to_dwh(extract_product_data(), 'dim_product')
  )

  load_dim_order = PythonOperator(
    task_id='load_dim_order',
    python_callable=lambda: load_to_dwh(extract_order_data(), 'dim_order')
  )

  load_dim_order_item = PythonOperator(
    task_id='load_dim_order_item',
    python_callable=lambda: load_to_dwh(extract_order_items_data(), 'dim_order_item')
  )

  load_dim_seller = PythonOperator(
    task_id='load_dim_seller',
    python_callable=lambda: load_to_dwh(extract_seller_data(), 'dim_seller')
  )

  load_dim_date = PythonOperator(
    task_id='load_dim_date',
    python_callable=lambda: load_to_dwh(dim_date(), 'dim_date')
  )

  load_fact_table = PythonOperator(
    task_id='load_fact_table',
    python_callable=lambda: load_to_dwh(extract_fact_sales(), 'fact_sales')
  )

  create__stage_tables >> extract_data_from_csv_to_staging >> [load_dim_customer, load_dim_product, load_dim_order, load_dim_order_item, load_dim_date, load_dim_seller] >> load_fact_table
