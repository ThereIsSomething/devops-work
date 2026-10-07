data "azurerm_resource_group" "lab" { name = var.resource_group_name }
resource "azurerm_storage_account" "lab" {
  name                            = var.storage_account_name
  resource_group_name             = data.azurerm_resource_group.lab.name
  location                        = data.azurerm_resource_group.lab.location
  account_tier                    = "Standard"
  account_replication_type        = "LRS"
  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = false
  shared_access_key_enabled       = false
  blob_properties { versioning_enabled = true }
  tags = { student = "24BCS10589", stage = var.stage }
}
resource "azurerm_storage_container" "homework" {
  name                  = "homework"
  storage_account_id    = azurerm_storage_account.lab.id
  container_access_type = "private"
}
resource "azurerm_storage_blob" "evidence" {
  name                   = "hello.txt"
  storage_account_name   = azurerm_storage_account.lab.name
  storage_container_name = azurerm_storage_container.homework.name
  type                   = "Block"
  source_content         = "Terraform storage exercise by Nitish Kumar Bhambu, 24BCS10589.\n"
}
