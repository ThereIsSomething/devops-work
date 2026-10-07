output "storage_account" { value = azurerm_storage_account.lab.name }
output "blob_url" { value = azurerm_storage_blob.evidence.url }
