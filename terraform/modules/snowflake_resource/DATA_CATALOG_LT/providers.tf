terraform {
  required_version = "~> 1.5.0"
  required_providers {
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "~> 0.87.2"
    }
  }
}

provider "snowflake" {
  profile = "prod"
  role    = "ACCOUNTADMIN"
}