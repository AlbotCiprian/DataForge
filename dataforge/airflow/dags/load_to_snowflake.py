from __future__ import annotations

import datetime as dt
import os
from airflow import DAG
from airflow.operators.python import PythonOperator


def load_stub() -> None:
    # This task simulates loading transformed data into Snowflake.
    # If SNOWFLAKE credentials exist, it will attempt a lightweight connection.
    acct = os.environ.get("SNOWFLAKE_ACCOUNT")
    user = os.environ.get("SNOWFLAKE_USER")
    pwd = os.environ.get("SNOWFLAKE_PASSWORD")
    if not all([acct, user, pwd]):
        print("Snowflake env not set; skipping actual load.")
        return
    try:
        import snowflake.connector as sf

        conn = sf.connect(
            account=acct,
            user=user,
            password=pwd,
            warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
            database=os.environ.get("SNOWFLAKE_DATABASE", "DATAFORGE"),
            schema=os.environ.get("SNOWFLAKE_SCHEMA", "PUBLIC"),
        )
        with conn.cursor() as cur:
            cur.execute("select current_version()")
            print("Connected to Snowflake, version:", cur.fetchone())
    except Exception as e:
        print("Snowflake connection failed:", e)


with DAG(
    dag_id="load_to_snowflake",
    start_date=dt.datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    load = PythonOperator(task_id="load_to_snowflake", python_callable=load_stub)

