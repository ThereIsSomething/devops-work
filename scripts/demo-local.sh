#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export TASKBOARD_DB_PASSWORD=${TASKBOARD_DB_PASSWORD:-classroom-example-only}
docker compose -f demo-app/docker/compose.yaml up --build -d
curl --retry 20 --retry-connrefused --retry-delay 2 --fail http://127.0.0.1:13000/health
curl --fail http://127.0.0.1:13000/api/tasks
minikube ssh -- 'sudo crictl pull docker.io/library/postgres:16-alpine'
minikube image load homework-taskboard-backend:local
minikube image load homework-taskboard-frontend:local
scripts/kubectl create namespace homework-final --dry-run=client -o yaml | scripts/kubectl apply -f -
scripts/kubectl apply -f demo-app/kubernetes/secret.example.yaml
helm upgrade --install taskboard demo-app/helm/taskboard -n homework-final --set postgresImage=docker.io/library/postgres:16-alpine --set postgresImagePullPolicy=IfNotPresent --wait --wait-for-jobs --timeout 300s
scripts/kubectl -n homework-final get pods,svc,pvc,hpa,ingress
