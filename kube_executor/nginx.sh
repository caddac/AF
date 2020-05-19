#!/usr/bin/env bash -euo pipefail

source ./functions.sh

#nginx ingress controller
install_repo "ingress-nginx" "https://kubernetes.github.io/ingress-nginx"
helm upgrade --install --atomic nginx ingress-nginx/ingress-nginx