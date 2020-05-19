from datetime import datetime

from airflow import DAG
from airflow.operators.http_operator import SimpleHttpOperator

with DAG(dag_id='firstDag',
         description='runs a dag',
         schedule_interval='0 0 * * *',
         start_date=datetime(2019, 1, 1),
         catchup=False) as d:
  get_time = SimpleHttpOperator(
      task_id="get_time_to_xcom",

      http_conn_id='world_time',
      endpoint='/api/timezone/America/Boise',
      method='GET',
      xcom_push=True)
