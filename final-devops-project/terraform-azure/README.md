# Real Azure AKS alternative

**Nitish Kumar Bhambu — 24BCS10589**

This project provisioned a real one-node AKS cluster in `rg-devops-homework`, Central India. The node used Standard_D2s_v3 and Kubernetes v1.35.8. Entra authentication and Azure RBAC are enabled, local administrator accounts are disabled, and the API is limited to trusted source CIDRs. The Free control-plane tier still has chargeable worker, disk and network resources.

The AWS EKS source is retained in `../terraform/` and validated, but it was not applied. Azure is an explicit provider substitution and instructor acceptance is still unknown.

Terraform also creates a user-assigned managed identity, a GitHub federated identity credential and two cluster-scoped role assignments for Actions. The local user receives AKS RBAC Cluster Admin to install coursework components. Creating role assignments requires permission beyond ordinary Contributor.

## Connect locally

Use an isolated kubeconfig so Minikube remains the default:

```bash
export TF_VAR_subscription_id="$(az account show --query id -o tsv)"
export TF_VAR_api_allowed_cidrs='["YOUR_PUBLIC_IP/32"]'
terraform init
terraform fmt
terraform validate
terraform plan -out=lab.tfplan
terraform apply lab.tfplan
az aks get-credentials -g rg-devops-homework -n aks-devops-homework --file /tmp/homework-aks-kubeconfig
KUBECONFIG=/tmp/homework-aks-kubeconfig kubelogin convert-kubeconfig -l azurecli
KUBECONFIG=/tmp/homework-aks-kubeconfig kubectl get nodes
```

[AKS deployment and node results](../README.md#aks-node)

## Hosted deployment identity

The Actions workflow uses OIDC instead of an Azure client secret. Its trust is restricted to this repository's `main` branch. The first login failed because this repository uses GitHub's immutable OIDC subject, with owner/repository IDs. Updating the federated credential to match the issued subject fixed that configuration. See [GitHub's immutable-subject documentation](https://docs.github.com/en/actions/reference/security/oidc).

Repository variables hold the client, tenant and subscription identifiers and original API CIDR; they are identifiers rather than credentials. The workflow temporarily adds its runner IP and restores the original allowlist afterward. The built-in GitHub token pulls the private GHCR images during this disposable deployment; it expires and is not a suitable permanent cluster pull credential.

After provisioning, configure the repository identifiers from the new Terraform outputs, then dispatch the deployment with a successful CI image commit:

```bash
gh variable set AZURE_CLIENT_ID --body "$(terraform output -raw github_client_id)"
gh variable set AZURE_TENANT_ID --body "$(terraform output -raw tenant_id)"
gh variable set AZURE_SUBSCRIPTION_ID --body "$(az account show --query id -o tsv)"
gh variable set AZURE_API_CIDR --body 'YOUR_PUBLIC_IP/32'
gh workflow run azure-deploy.yml -f image_tag=FULL_SUCCESSFUL_CI_COMMIT_SHA
```

The lab's repository variables are removed during cleanup because its managed identity no longer exists. Recreate the infrastructure and repopulate them before another cloud deployment.

The deployment uses the AKS `managed-csi` storage class, the exact published commit tags, the separately created classroom Secret and Traefik. Monitoring is installed in an internal namespace. Cleanup destroys the AKS cluster, managed node resources, OIDC identity and lab group after evidence collection.

References: [AKS Azure RBAC](https://learn.microsoft.com/azure/aks/manage-azure-rbac), [Azure managed identity federation](https://learn.microsoft.com/entra/workload-id/workload-identity-federation).

## Local validation

The commands below ran from this Terraform project folder. Validation checks configuration; it does not provision cloud resources.

```bash
Initializing provider plugins...
- Finding hashicorp/azurerm versions matching "~> 4.0"...
- Installing hashicorp/azurerm v4.81.0...
- Installed hashicorp/azurerm v4.81.0 (signed by HashiCorp)

Terraform has created a lock file .terraform.lock.hcl to record the provider
# ... intermediate output omitted ...
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
Success! The configuration is valid.
```
