resource "azurerm_subnet" "app" {
  name                 = "app"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.1.0/24"]
  delegation {
    name = "delegation"
    service_delegation {
      name = "Microsoft.Web/serverFarms"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/action",
      ]
    }
  }
}

resource "azurerm_service_plan" "main" {
  name                = var.project_name
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Linux"
  sku_name            = var.app.sku_name
}

resource "azurerm_linux_web_app" "main" {
  name                      = var.project_name
  resource_group_name       = azurerm_resource_group.main.name
  location                  = azurerm_service_plan.main.location
  service_plan_id           = azurerm_service_plan.main.id
  virtual_network_subnet_id = azurerm_subnet.app.id
  https_only                = true

  app_settings = {
    DATABASE_HOST                         = azurerm_postgresql_flexible_server.main.fqdn
    DATABASE_MS_ENTRA_AUTH_PRINCIPAL_NAME = var.project_name
    DOCKER_ENABLE_CI                      = true
    WEBSITES_ENABLE_APP_SERVICE_STORAGE   = false
  }

  identity {
    type = "SystemAssigned"
  }

  site_config {
    container_registry_use_managed_identity = true

    application_stack {
      docker_registry_url = "https://${azurerm_container_registry.main.login_server}"
      docker_image_name   = var.app.container_image
    }
  }

  logs {
    http_logs {
      file_system {
        retention_in_days = 60
        retention_in_mb   = 100
      }
    }
  }
}

resource "azurerm_role_assignment" "app_to_acr" {
  scope                = azurerm_container_registry.main.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_linux_web_app.main.identity.0.principal_id
}
