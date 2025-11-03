output "airflow_role_arn" {
  value = aws_iam_role.airflow.arn
}

output "dbt_role_arn" {
  value = aws_iam_role.dbt.arn
}

