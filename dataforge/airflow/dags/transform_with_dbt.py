from __future__ import annotations

import datetime as dt
import os
from airflow import DAG
from airflow.operators.bash import BashOperator


DBT_PROJECT_DIR = os.environ.get("DBT_PROJECT_DIR", "/opt/airflow/dbt")
DBT_PROFILES_DIR = os.environ.get("DBT_PROFILES_DIR", "/opt/airflow/dbt")

default_args = {
    "owner": "dataops",
    "retries": 0,
}

with DAG(
    dag_id="transform_with_dbt",
    start_date=dt.datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args,
) as dag:

    dbt_run = BashOperator(
        task_id="dbt_run_staging",
        bash_command=f"dbt run --project-dir {DBT_PROJECT_DIR} --profiles-dir {DBT_PROFILES_DIR} --select tag:staging",
        env={
            "DBT_PROJECT_DIR": DBT_PROJECT_DIR,
            "DBT_PROFILES_DIR": DBT_PROFILES_DIR,
        },
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"dbt test --project-dir {DBT_PROJECT_DIR} --profiles-dir {DBT_PROFILES_DIR}",
        env={
            "DBT_PROJECT_DIR": DBT_PROJECT_DIR,
            "DBT_PROFILES_DIR": DBT_PROFILES_DIR,
        },
    )

    dbt_run >> dbt_test

