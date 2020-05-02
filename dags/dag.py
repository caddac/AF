from datetime import datetime

from airflow import DAG
from airflow.operators.http_operator import SimpleHttpOperator

with DAG('firstDag', 'runs a dag', '0 0 * * *', start_date=datetime(2019, 1, 1), ):
  get_time = SimpleHttpOperator(
      task_id="get_time_to_xcom",

      http_conn_id='world_time',
      endpoint='/api/timezone/America/Boise',
      method='GET',
      xcom_push=True)
