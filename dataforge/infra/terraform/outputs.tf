output "raw_bucket_name" {
  value = module.s3_raw.bucket_name
}

output "airflow_role_arn" {
  value = module.iam.airflow_role_arn
}

output "dbt_role_arn" {
  value = module.iam.dbt_role_arn
}

