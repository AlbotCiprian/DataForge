variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "raw_bucket_name" {
  description = "Raw S3 bucket name"
  type        = string
}

variable "airflow_role_name" {
  description = "IAM role name for Airflow"
  type        = string
  default     = "dataforge-airflow-role"
}

variable "dbt_role_name" {
  description = "IAM role name for dbt"
  type        = string
  default     = "dataforge-dbt-role"
}

variable "snowflake_user" {
  description = "Snowflake integration user"
  type        = string
  default     = "SVC_DBT"
}

variable "snowflake_role" {
  description = "Snowflake default role"
  type        = string
  default     = "TRANSFORMER"
}

variable "snowflake_warehouse" {
  description = "Snowflake warehouse"
  type        = string
  default     = "COMPUTE_WH"
}

