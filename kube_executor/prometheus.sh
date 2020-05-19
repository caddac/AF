#!/usr/bin/env bash -euo pipefail

source ./functions.sh

helm upgrade --install --atomic prometheus stable/prometheus -f install/prometheus_local.yml
