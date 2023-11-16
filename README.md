# Terraform Azure Webapp

## Deploy to Azure

### 1. Prepare Azure
1. Prepare Azure tenant and subscription
2. Create below resources to store tfstate
    1. Resource Group
    2. Storage Account
    3. Blob Container
3. Create service principal for Terraform
    1. Create Entra ID application
    2. Create client secret
    3. Assign the subscription's "Contributor" role to the application

### 2. Prepare var files
Create the following two configuration files.

`terraform/production.tfbackend`

``` tfvars
resource_group_name  = "my-project-tfstate"
storage_account_name = "tfstate01234567"
container_name       = "tfstate"
key                  = "production.tfstate"
```

`terraform/production.tfvars`

``` tfvars
project_name = "my-project-production"

region = "japaneast"

azure = {
  tenant_id       = "..."
  subscription_id = "..."
  service_principal = {
    client_id     = "..."
    client_secret = "..."
  }
}

container_registry = {
  name = "..."
}

app = {}

database = {}
```

### 3. Apply
``` console
$ terraform init -backend-config=production.tfbackend
```

``` console
$ terraform plan -var-file=production.tfvars
```

``` console
$ terraform apply -var-file=production.tfvars
```

### 4. Do some operations manually in Azure Portal
- Add the app service as Microsoft Entra administrator to the database auth settings
- Connect to the database as an administrator user
  - Change initial password
  - Grant privileges to app service role
    - `GRANT ALL PRIVILEGES ON DATABASE <DB_NAME> TO "<SERVICE_PRINCIPAL_NAME>";`
    - `GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "<SERVICE_PRINCIPAL_NAME>";`
- Build and push application to ACR