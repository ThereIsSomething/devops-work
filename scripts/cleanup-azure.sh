#!/usr/bin/env bash
set -euo pipefail
# Use each project's terraform destroy first so its state records cleanup.
# This final sweep removes the shared bootstrap group and any owned remnants.
az group delete --name rg-devops-homework --yes
az resource list --query '[].{name:name,type:type,resourceGroup:resourceGroup}' -o json
az group list --query '[].name' -o json

# Azure may create this group automatically when the first VNet is provisioned.
# For this homework the recorded subscription baseline was empty.
# Do not use this optional sweep on a pre-existing shared subscription.
if [[ "${HOMEWORK_EMPTY_AZURE_BASELINE:-false}" == true ]] && [[ "$(az group exists --name NetworkWatcherRG)" == true ]]; then
  az group delete --name NetworkWatcherRG --yes
  az resource list --query '[].{name:name,type:type,resourceGroup:resourceGroup}' -o json
  az group list --query '[].name' -o json
fi
