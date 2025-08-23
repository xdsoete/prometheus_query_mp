#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail

# PROMETHEUS
if kubectl get pods | grep -q prometheus; then
  echo ">> Prometheus already installed"
else
  echo ">> installing Prometheus"
  helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
  helm repo update

  helm install prometheus prometheus-community/kube-prometheus-stack
fi

# VICTORIA
#if kubectl get pods | grep -q victoria-metrics; then
#  echo ">> VictoriaMetrics already installed"
#else
#  echo ">> Installing VictoriaMetrics"
#  helm repo add vm https://victoriametrics.github.io/helm-charts/
#  helm repo update

#  helm install vmks vm/victoria-metrics-k8s-stack
#fi

pushd prom_query
mkdir -p bin/

echo ">> Build the docker image for the query server"

docker build -t "xdsoete/prom_query:latest" .
docker push xdsoete/prom_query:latest

kubectl apply -f deployment.yaml

popd
