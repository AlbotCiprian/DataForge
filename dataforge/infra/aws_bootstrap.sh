#!/usr/bin/env bash
set -euo pipefail

echo "[aws_bootstrap] Checking AWS CLI..."
if ! command -v aws >/dev/null 2>&1; then
  echo "AWS CLI not found. Please install and configure credentials." >&2
  exit 1
fi

RAW_BUCKET=${AWS_S3_RAW_BUCKET:-dataforge-raw-example}
REGION=${AWS_REGION:-us-east-1}

echo "[aws_bootstrap] Creating S3 bucket: ${RAW_BUCKET} in ${REGION} (idempotent)"
aws s3api create-bucket \
  --bucket "${RAW_BUCKET}" \
  --region "${REGION}" \
  --create-bucket-configuration LocationConstraint="${REGION}" 2>/dev/null || true

echo "[aws_bootstrap] Enabling versioning"
aws s3api put-bucket-versioning --bucket "${RAW_BUCKET}" --versioning-configuration Status=Enabled

echo "[aws_bootstrap] Done."

