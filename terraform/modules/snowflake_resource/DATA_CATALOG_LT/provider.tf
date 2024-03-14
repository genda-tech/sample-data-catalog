terraform {
  required_version = "~> 1.5.0"
  required_providers {
    snowflake = {
      source  = "registry.terraform.io/Snowflake-Labs/snowflake"
      version = "~> 0.71.0"
    }
  }
}

provider "snowflake" {
  profile = "prod"
  role    = "ACCOUNTADMIN"
}
