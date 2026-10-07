output "resource_group" { value = data.azurerm_resource_group.lab.name }
output "vnet_id" { value = azurerm_virtual_network.lab.id }
output "storage_account" { value = azurerm_storage_account.lab.name }
