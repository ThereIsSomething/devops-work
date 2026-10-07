data "azurerm_resource_group" "lab" {
  name = var.resource_group_name
}
resource "azurerm_virtual_network" "lab" {
  name                = "vnet-devops-homework"
  address_space       = ["10.40.0.0/16"]
  location            = data.azurerm_resource_group.lab.location
  resource_group_name = data.azurerm_resource_group.lab.name
}
resource "azurerm_subnet" "app" {
  name                 = "application"
  resource_group_name  = data.azurerm_resource_group.lab.name
  virtual_network_name = azurerm_virtual_network.lab.name
  address_prefixes     = ["10.40.1.0/24"]
}
resource "azurerm_network_security_group" "app" {
  name                = "nsg-devops-homework"
  location            = data.azurerm_resource_group.lab.location
  resource_group_name = data.azurerm_resource_group.lab.name
}
resource "azurerm_subnet_network_security_group_association" "app" {
  subnet_id                 = azurerm_subnet.app.id
  network_security_group_id = azurerm_network_security_group.app.id
}
resource "azurerm_storage_account" "lab" {
  name                            = var.storage_account_name
  resource_group_name             = data.azurerm_resource_group.lab.name
  location                        = data.azurerm_resource_group.lab.location
  account_tier                    = "Standard"
  account_replication_type        = "LRS"
  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = false
  shared_access_key_enabled       = false
}
