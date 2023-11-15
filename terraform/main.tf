resource "azurerm_resource_group" "main" {
  name     = var.project_name
  location = var.region
}

resource "azurerm_virtual_network" "main" {
  name                = var.project_name
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  address_space       = ["10.0.0.0/16"]
}
