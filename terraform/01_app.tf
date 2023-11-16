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
    DATABASE_HOST                       = azurerm_postgresql_flexible_server.main.fqdn
    WEBSITES_ENABLE_APP_SERVICE_STORAGE = false
  }

  identity {
    type = "SystemAssigned"
  }

  site_config {
    application_stack {
      docker_registry_url      = "https://${azurerm_container_registry.main.login_server}"
      docker_registry_username = azurerm_container_registry.main.admin_username
      docker_registry_password = azurerm_container_registry.main.admin_password
      docker_image_name        = var.app.container_image
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