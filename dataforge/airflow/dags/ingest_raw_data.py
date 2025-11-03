from __future__ import annotations

import csv
import datetime as dt
import os
from pathlib import Path
from typing import Optional

import requests
from airflow import DAG
from airflow.operators.python import PythonOperator


DATA_DIR = Path(os.environ.get("DATA_DIR", "/opt/data"))
RAW_DIR = DATA_DIR / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


def fetch_csv(output_path: str, url: Optional[str] = None) -> None:
    url = url or "https://people.sc.fsu.edu/~jburkardt/data/csv/airtravel.csv"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        content = resp.text
    except Exception:
        # Offline fallback: synthesize a tiny CSV
        content = "year,month,passengers\n2024,01,100\n2024,02,120\n"

    with open(output_path, "w", newline="") as f:
        f.write(content)


default_args = {
    "owner": "dataops",
    "retries": 1,
    "retry_delay": dt.timedelta(minutes=5),
}

with DAG(
    dag_id="ingest_raw_data",
    start_date=dt.datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args,
) as dag:

    def _ingest():
        ts = dt.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        out = RAW_DIR / f"airtravel_{ts}.csv"
        fetch_csv(str(out))

    ingest = PythonOperator(
        task_id="fetch_and_store_csv",
        python_callable=_ingest,
    )

