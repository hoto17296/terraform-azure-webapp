# Terraform Azure Webapp

## Develop application

### Start dev server
``` console
$ docker compose up
```

### Run test
``` console
$ docker compose exec app python -m pytest
```

## Deploy to Azure

### 1. Prepare Azure
1. Prepare Azure tenant and subscription
2. Create below resources to store tfstate
    1. Resource Group (e.g. `my-project-tfstate`)
    2. Storage Account (e.g. `tfstate01234567`)
    3. Blob Container (e.g. `tfstate`)
3. Create service principal for Terraform
    1. Create Entra ID application (e.g. `my-project-terraform`)
    2. Create client secret
    3. Assign the subscription's **"Owner"** role to the application
        - "Owner" is required because "Contributor" can't assign roles to resources

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
  name = "myprojectproduction"
}

app = {}

database = {}
```

### 3. Apply
``` console
$ terraform -chdir=./terraform init -backend-config=production.tfbackend
```

``` console
$ terraform -chdir=./terraform plan -var-file=production.tfvars
```

``` console
$ terraform -chdir=./terraform apply -var-file=production.tfvars
```

### 4. Do some operations manually in Azure Portal

#### 4.1 Build and push application to ACR
```
az acr build --registry ${registry_name} --image app ./app
```

#### 4.2 Add the app service as Microsoft Entra administrator to the database auth settings
```
az postgres flexible-server ad-admin create --resource-group ${project_name} --server-name ${project_name} --display-name ${project_name} --object-id ${app_service_object_id} --type ServicePrincipal
```

#### 4.3 Connect to the database and modify settings
1. Create an SSH tunnel to the App Service container
    - `az webapp create-remote-connection --subscription ${subscription_id} --resource-group ${resource_group_name} -n ${app_service_name}`
2. Connect to the database as an administrator user via the SSH tunnel
3. Modify database settings
    - Change administrator user's initial password
        - `ALTER USER postgres WITH PASSWORD '<NEW_PASSWORD>'`
    - Grant privileges to app service role
        - `GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO "${SERVICE_PRINCIPAL_NAME}";`
        - `GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "${SERVICE_PRINCIPAL_NAME}";`
        - `ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO "${SERVICE_PRINCIPAL_NAME}";`
    - Create tables
        - → [database/initdb.d/ddl.sql](database/initdb.d/ddl.sql)

