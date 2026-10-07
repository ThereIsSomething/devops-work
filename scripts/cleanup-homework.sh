#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
# Deliberately limited to the namespaces created for this submission.
for n in 09 10 11 12 13 14 15; do
  scripts/kubectl delete namespace "homework-s$n" --ignore-not-found --wait=false
done
scripts/kubectl delete namespace homework-final homework-monitoring homework-gitops homework-ingress --ignore-not-found --wait=false
TASKBOARD_DB_PASSWORD=classroom-example-only docker compose -f final-devops-project/docker/compose.yaml down
# Persistent Compose data is retained. Remove the named homework volume separately only when no longer needed.
