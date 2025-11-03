resource "snowflake_user" "dbt" {
  name         = var.user_name
  default_role = var.default_role
  default_warehouse = var.default_warehouse
  must_change_password = false
}

