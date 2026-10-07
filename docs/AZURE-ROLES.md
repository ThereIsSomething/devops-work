# Azure roles for this homework

We use the student's local `az login` session. There is no separate assistant account to invite and no reason to paste passwords, client secrets, tokens or private keys into chat.

| Role | Scope | When needed |
|---|---|---|
| Contributor | Dedicated resource group, e.g. rg-devops-homework | Create/update/delete the Terraform-managed storage account, VNet, VM and AKS cluster |
| Storage Blob Data Contributor | Specific storage account or container | Blob operations and AzureRM data-plane checks when shared-key access is disabled |
| Azure Kubernetes Service RBAC Cluster Admin | Specific AKS cluster | Install namespace-level and cluster-level coursework components after connecting to an Entra/Azure-RBAC-enabled cluster |
| Azure Kubernetes Service Cluster User Role | Specific AKS cluster | Retrieve user kubeconfig when a narrower identity lacks that permission; Contributor already includes cluster-management actions |
| Role Based Access Control Administrator | Lab resource group, only if needed | Let Terraform create role assignments; an existing administrator can make the assignments instead |

**Minimum for the first storage/network/VM exercise:** Contributor on an existing lab group. A subscription administrator can create the group and register the Microsoft.Storage, Microsoft.Network, Microsoft.Compute and Microsoft.ContainerService resource providers as needed. Resource-provider registration is subscription-scoped and is not guaranteed by Contributor on a resource group.

No subscription-wide Owner or Entra Global Administrator role is needed for this setup. This implementation uses a user-assigned managed identity and a GitHub federated identity credential in the lab resource group; it does not require an Entra app registration. The GitHub identity receives Azure Kubernetes Service Contributor Role and Azure Kubernetes Service RBAC Cluster Admin on the single lab cluster. Terraform needs role-assignment permission to grant those roles.

## Assign the role in Azure Portal

1. Search **Resource groups** and open the dedicated lab group.
2. Open **Access control (IAM) → Add → Add role assignment**.
3. Select **Contributor**, then **Next**.
4. Under **Assign access to**, choose **User, group, or service principal**.
5. Choose **Select members**, select the account used by local `az login`, and save the selection.
6. Choose **Review + assign**. You need role-assignment permission to do this; otherwise ask the existing administrator.
7. Use **Check access / View my access** to confirm. Existing subscription-scope roles may already cover the group; avoid redundant assignments.

For AKS, grant the Kubernetes RBAC role on the cluster after it exists. For Blob data access, grant the data role on the storage account after it exists. Keep those scopes narrow.

Sources: [Privileged built-in roles](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles/privileged), [Blob data role assignment](https://learn.microsoft.com/azure/storage/blobs/assign-azure-role-data-access), [AKS Azure RBAC](https://learn.microsoft.com/azure/aks/manage-azure-rbac).
