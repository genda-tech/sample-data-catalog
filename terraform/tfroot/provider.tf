terraform {
  required_version = "~> 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.41.0"
    }
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "~> 0.87.2"
    }
  }
}

provider "aws" {
  region = "ap-northeast-1"
}

provider "snowflake" {
  profile = "prod"
  role    = "ACCOUNTADMIN"
}