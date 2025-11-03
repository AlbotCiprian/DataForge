terraform {
  required_version = ">= 1.8.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = ">= 0.96.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

module "s3_raw" {
  source      = "./modules/s3_bucket"
  bucket_name = var.raw_bucket_name
  versioning  = true
}

module "iam" {
  source                 = "./modules/iam_roles"
  raw_bucket_arn         = module.s3_raw.bucket_arn
  airflow_role_name      = var.airflow_role_name
  dbt_role_name          = var.dbt_role_name
}

provider "snowflake" {}

module "snowflake_integration" {
  source              = "./modules/snowflake_integration"
  user_name           = var.snowflake_user
  default_role        = var.snowflake_role
  default_warehouse   = var.snowflake_warehouse
}

