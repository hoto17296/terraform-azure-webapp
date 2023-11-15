variable "project_name" {
  type = string
  validation {
    condition     = can(regex("^[0-9a-z-]+$", var.project_name))
    error_message = "This value can only contain alphanumeric characters and hyphens."
  }
}

variable "region" {
  type = string
}

variable "azure" {
  type = object({
    tenant_id       = string
    subscription_id = string
    service_principal = object({
      client_id     = string
      client_secret = string
    })
  })
}

variable "container_registry" {
  type = object({
    name = string
    sku  = optional(string, "Basic")
  })
}

variable "database" {
  type = object({
    administrator_login    = optional(string, "postgres")
    administrator_password = optional(string, "deadbeef")
    sku_name               = optional(string, "B_Standard_B1ms")
    storage_mb             = optional(number, 32768)
    version                = optional(string, "15")
  })
}
