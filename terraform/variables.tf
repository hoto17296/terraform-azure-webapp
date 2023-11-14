variable "project_name" {
  type = string
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
