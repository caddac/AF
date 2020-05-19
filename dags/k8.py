import os
from time import sleep

import pandas
from airflow import DAG
from datetime import datetime, timedelta

from airflow.contrib.kubernetes.volume import Volume
from airflow.contrib.kubernetes.volume_mount import VolumeMount
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 1),
    'catchup': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=6)
}

dag = DAG('etl_example', default_args=default_args, schedule_interval=None)

get_file = SimpleHttpOperator(task_id='download_data',
                              http_conn_id='json_placeholder_conn',
                              method='GET',
                              endpoint='posts',
                              xcom_push=True,
                              dag=dag)


def write_data(**context):
    ti = context['task_instance']
    data = ti.xcom_pull(task_ids='download_data')
    dir_name = f'/usr/local/airflow/work/{dag.dag_id}/{ti.execution_date}'
    # Create target directory & all intermediate directories if don't exists
    try:
        os.makedirs(dir_name)
        print("Directory ", dir_name, " Created ")
    except FileExistsError:
        print("Directory ", dir_name, " already exists")

        # print(data)
    with open(file=f'{dir_name}/data.json', mode='w') as f:
        lines = f.write(data)
        print(f'wrote {lines} lines to the file')
        f.close()


write_xcom_to_work = PythonOperator(task_id='write_data_to_work_dir',
                                    python_callable=write_data,
                                    provide_context=True,
                                    dag=dag,
                                    )

volume_mount = VolumeMount('work-volume',
                           mount_path='/work',
                           sub_path=None,
                           read_only=False)

volume_config = {
    'persistentVolumeClaim':
        {
            'claimName': 'work-claim'
        }
}
volume = Volume(name='work-volume', configs=volume_config)

validate_file = KubernetesPodOperator(namespace='default',
                                      image="v:latest",
                                      # cmds=["python", "--version"],
                                      arguments=[f"{dag.dag_id}/{{{{ts}}}}/data.json",
                                                 f"{dag.dag_id}/{{{{ts}}}}/output.txt"],
                                      # labels={"foo": "bar"},
                                      name="validate_file",
                                      task_id="validate_file",
                                      get_logs=True,
                                      dag=dag,
                                      is_delete_operator_pod=True,
                                      volumes=[volume],
                                      volume_mounts=[volume_mount],
                                      security_context={
                                          'privileged': 'true'
                                      },
                                      )

get_file >> write_xcom_to_work >> validate_file

# def call_me():
#     for i in range(1, 3):
#         print(f"{i}/3")
#         sleep(1)


# start = PythonOperator(task_id='wait_3_sec', python_callable=call_me, dag=dag)
#
# passing = KubernetesPodOperator(namespace='default',
#                                 image="python:slim-buster",
#                                 cmds=["python", "--version"],
#                                 # arguments=["print('hello world')"],
#                                 labels={"foo": "bar"},
#                                 name="passing-test",
#                                 task_id="passing-task",
#                                 get_logs=True,
#                                 dag=dag,
#                                 )
#
# failing = KubernetesPodOperator(namespace='default',
#                                 image="pythonversion:latest",
#                                 # cmds=["python", "-c"],
#                                 # arguments=["print('hello world')"],
#                                 labels={"foo": "bar"},
#                                 name="fail",
#                                 task_id="failing-task",
#                                 get_logs=True,
#                                 dag=dag,
#                                 )
#
# passing.set_upstream(start)
# failing.set_upstream(start)
