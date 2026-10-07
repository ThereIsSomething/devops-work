#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
curl -fLsS https://raw.githubusercontent.com/argoproj/argo-cd/v3.5.4/manifests/core-install.yaml -o /tmp/homework-argocd-core.yaml
# The upstream manifest contains explicit namespace references in RBAC subjects.
sed 's/namespace: argocd/namespace: homework-gitops/g' /tmp/homework-argocd-core.yaml > /tmp/homework-argocd-custom.yaml
scripts/kubectl create namespace homework-gitops --dry-run=client -o yaml | scripts/kubectl apply -f -
scripts/kubectl -n homework-gitops apply --server-side -f /tmp/homework-argocd-custom.yaml
scripts/kubectl apply -f 19-monitoring-gitops/gitops/project.yaml
scripts/kubectl apply -f 19-monitoring-gitops/gitops/application.yaml
scripts/kubectl -n homework-gitops get applications
