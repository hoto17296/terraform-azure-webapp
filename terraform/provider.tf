terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>2.0"
    }
  }
  backend "azurerm" {}
}

provider "azurerm" {
  features {}
  tenant_id       = var.azure.tenant_id
  subscription_id = var.azure.subscription_id
  client_id       = var.azure.service_principal.client_id
  client_secret   = var.azure.service_principal.client_secret
}
