#!/usr/bin/env bash
set -euo pipefail

export PYTHONUNBUFFERED=1
export DATA_DIR=${DATA_DIR:-$(pwd)/data}

echo "[local_run] Writing sample data to ${DATA_DIR}/raw"
mkdir -p "${DATA_DIR}/raw"
python scripts/load_sample_data.py

echo "[local_run] Starting API on http://localhost:8000"
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

