resource "azurerm_user_assigned_identity" "github" {
  name                = "id-homework-github"
  location            = data.azurerm_resource_group.lab.location
  resource_group_name = data.azurerm_resource_group.lab.name
}
resource "azurerm_federated_identity_credential" "github_main" {
  name                = "github-main"
  resource_group_name = data.azurerm_resource_group.lab.name
  parent_id           = azurerm_user_assigned_identity.github.id
  audience            = ["api://AzureADTokenExchange"]
  issuer              = "https://token.actions.githubusercontent.com"
  subject             = "repo:ThereIsSomething/devops-work:ref:refs/heads/main"
}
resource "azurerm_role_assignment" "github_control" {
  scope                = azurerm_kubernetes_cluster.lab.id
  role_definition_name = "Azure Kubernetes Service Contributor Role"
  principal_id         = azurerm_user_assigned_identity.github.principal_id
}
resource "azurerm_role_assignment" "github_kubernetes" {
  scope                = azurerm_kubernetes_cluster.lab.id
  role_definition_name = "Azure Kubernetes Service RBAC Cluster Admin"
  principal_id         = azurerm_user_assigned_identity.github.principal_id
}
output "github_client_id" { value = azurerm_user_assigned_identity.github.client_id }
output "tenant_id" { value = data.azurerm_client_config.current.tenant_id }
