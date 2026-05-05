terraform {
  required_version = ">= 1.5.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
  backend "azurerm" {
    resource_group_name  = "educloud-tfstate-rg"
    storage_account_name = "educloudtfstate"
    container_name       = "tfstate"
    key                  = "staging.terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}

variable "location" {
  default = "East US"
}

# 1. Resource Group
resource "azurerm_resource_group" "rg" {
  name     = "educloud-staging-rg"
  location = var.location
}

# 2. Azure Database for PostgreSQL Flexible Server
resource "azurerm_postgresql_flexible_server" "postgres" {
  name                   = "educloud-staging-psql"
  resource_group_name    = azurerm_resource_group.rg.name
  location               = azurerm_resource_group.rg.location
  version                = "16"
  administrator_login    = "psqladmin"
  administrator_password = var.db_password
  storage_mb             = 32768
  sku_name               = "B_Standard_B1ms"
}

resource "azurerm_postgresql_flexible_server_database" "db" {
  name      = "college_db"
  server_id = azurerm_postgresql_flexible_server.postgres.id
  collation = "en_US.utf8"
  charset   = "utf8"
}

# 3. Azure App Service Plan & Web App for Containers
resource "azurerm_service_plan" "asp" {
  name                = "educloud-staging-asp"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "app" {
  name                = "educloud-staging-app"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_service_plan.asp.location
  service_plan_id     = azurerm_service_plan.asp.id

  site_config {
    always_on = true
    application_stack {
      docker_image_name = "college-platform:staging"
    }
  }
}

variable "db_password" {
  type      = string
  sensitive = true
}

output "web_app_fqdn" {
  value = azurerm_linux_web_app.app.default_hostname
}
