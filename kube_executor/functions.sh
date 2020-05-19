function install_repo() {
  local name=$1
  local url=$2

  if [[ -z $(helm repo list | grep ${name}) ]]; then
    echo "adding ${name} repo"
    helm repo add ${name} ${url}
  else
    echo "${name} repo already added"
  fi
}

function create_namespace() {
  local name=$1
  if [[ -z $(kubectl get namespaces | grep ${name}) ]]; then
    echo "creating namespace: ${name}"
    kubectl create namespace ${name}
  fi
}