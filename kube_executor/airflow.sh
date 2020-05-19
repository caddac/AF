#!/usr/bin/env bash -euo pipefail

source ./functions.sh

create_namespace "airflow"
helm upgrade --install --atomic --namespace airflow airflow stable/airflow -f install/airflow_local.yml
