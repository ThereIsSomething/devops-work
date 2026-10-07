#!/usr/bin/env bash
set -euo pipefail
# Use each project's terraform destroy first so its state records cleanup.
# This final sweep removes the shared bootstrap group and any owned remnants.
az group delete --name rg-devops-homework --yes
az resource list --query '[].{name:name,type:type,resourceGroup:resourceGroup}' -o json
az group list --query '[].name' -o json
