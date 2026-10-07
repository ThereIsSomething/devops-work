terraform {
  required_version = ">= 1.7.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}
provider "azurerm" {
  features {}
  storage_use_azuread             = true
  subscription_id                 = var.subscription_id
  resource_provider_registrations = "none"
}
