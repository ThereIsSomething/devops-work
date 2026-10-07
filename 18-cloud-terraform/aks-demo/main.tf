resource "azurerm_kubernetes_cluster" "lab" {
  name                              = "aks-devops-homework"
  location                          = data.azurerm_resource_group.lab.location
  resource_group_name               = data.azurerm_resource_group.lab.name
  dns_prefix                        = "nitish-homework"
  sku_tier                          = "Free"
  role_based_access_control_enabled = true
  local_account_disabled            = true
  azure_active_directory_role_based_access_control {
    tenant_id          = data.azurerm_client_config.current.tenant_id
    azure_rbac_enabled = true
  }
  default_node_pool {
    name       = "system"
    node_count = 1
    vm_size    = var.node_vm_size
    upgrade_settings {
      max_surge = "10%"
    }
  }
  identity { type = "SystemAssigned" }
  network_profile {
    network_plugin      = "azure"
    network_plugin_mode = "overlay"
    load_balancer_sku   = "standard"
  }
  api_server_access_profile {
    authorized_ip_ranges = var.api_allowed_cidrs
  }
}
output "cluster_name" { value = azurerm_kubernetes_cluster.lab.name }
output "resource_group" { value = data.azurerm_resource_group.lab.name }

resource "azurerm_role_assignment" "cluster_admin" {
  scope                = azurerm_kubernetes_cluster.lab.id
  role_definition_name = "Azure Kubernetes Service RBAC Cluster Admin"
  principal_id         = data.azurerm_client_config.current.object_id
}
