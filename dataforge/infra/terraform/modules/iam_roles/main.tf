data "aws_iam_policy_document" "s3_rw_raw" {
  statement {
    actions   = ["s3:PutObject", "s3:GetObject", "s3:ListBucket"]
    resources = [var.raw_bucket_arn, "${var.raw_bucket_arn}/*"]
  }
}

resource "aws_iam_policy" "s3_rw" {
  name   = "dataforge-s3-rw"
  policy = data.aws_iam_policy_document.s3_rw_raw.json
}

resource "aws_iam_role" "airflow" {
  name               = var.airflow_role_name
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
      Action   = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "airflow_attach" {
  role       = aws_iam_role.airflow.name
  policy_arn = aws_iam_policy.s3_rw.arn
}

resource "aws_iam_role" "dbt" {
  name               = var.dbt_role_name
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action   = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "dbt_attach" {
  role       = aws_iam_role.dbt.name
  policy_arn = aws_iam_policy.s3_rw.arn
}

