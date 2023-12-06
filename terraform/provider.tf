terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.80"
    }
  }

  # Store tfstate to Azure Blob Storage
  backend "azurerm" {}

  # Store tfstate to local
  # backend "local" {}
}

# Authenticating to Azure using a Service Principal and a Client Secret
# https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/guides/service_principal_client_secret
provider "azurerm" {
  features {}
  tenant_id       = var.azure.tenant_id
  subscription_id = var.azure.subscription_id
  client_id       = var.azure.service_principal.client_id
  client_secret   = var.azure.service_principal.client_secret
}

# Authenticating to Azure using the Azure CLI
# https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/guides/azure_cli
# provider "azurerm" {
#   features {}
#   tenant_id       = var.azure.tenant_id
#   subscription_id = var.azure.subscription_id
# }
