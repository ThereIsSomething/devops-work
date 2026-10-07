# Azure AKS alternative

This provisions a real one-node AKS cluster in an existing lab resource group, using Entra authentication and Azure RBAC. It is an explicit alternative to the AWS EKS requirement. It is not a mock and is not yet provisioned. The Free control-plane tier does not make the worker VM, disks, public IPs or networking free.

Required: Contributor on the lab group; the Microsoft.ContainerService provider registered by a subscription administrator; sufficient regional VM quota; a reviewed budget. After creation, an administrator must grant your signed-in identity **Azure Kubernetes Service RBAC Cluster Admin** on this specific cluster (or a narrower Kubernetes role if appropriate). Contributor includes cluster management permissions but does not by itself give Kubernetes data-plane access or permission to create role assignments.

Use an isolated kubeconfig so Minikube remains the local default. The kubelogin tool may be required for the Entra exec login flow. Do not use --admin as a workaround for the cluster's disabled local accounts.

```bash
terraform init
terraform validate
terraform plan -out=tfplan
terraform apply tfplan
az aks get-credentials --resource-group rg-devops-homework --name aks-devops-homework --file /tmp/homework-aks-kubeconfig
KUBECONFIG=/tmp/homework-aks-kubeconfig kubectl get nodes
# Only after saving deployment evidence and reviewing the resources:
terraform destroy
```

The application Helm chart needs the AKS storage class (for example managed-csi), published GHCR image tags, an external Secret, a metrics API and an installed Ingress controller. Do not reuse Minikube-local image names on AKS.

Reference: [AKS Azure RBAC](https://learn.microsoft.com/azure/aks/manage-azure-rbac).
