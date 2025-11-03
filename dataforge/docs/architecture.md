# Architecture

This document explains how the platform components work together using an ELT pattern.

## Overview
- Extract + Load: Airflow ingests data and lands it into S3 (or local `data/raw` during development).
- Transform: dbt compiles and runs models in Snowflake, promoting from `staging` to curated `marts`.
- Orchestrate: Airflow DAGs coordinate ingestion and dbt runs.
- Serve: FastAPI exposes health and metadata endpoints for observability and integration.
- Provision: Terraform provisions AWS resources (S3, IAM) and Snowflake users/roles for integration.

## Data Flow
1. `ingest_raw_data.py` downloads or synthesizes CSVs and stores them in `s3://<raw-bucket>/domain/...` or local `data/raw/`.
2. `transform_with_dbt.py` invokes dbt to compile and run `staging` models, then tests.
3. `load_to_snowflake.py` (optional) pushes transformed tables to Snowflake or no-ops locally.

## Environments
- Local: docker-compose with Postgres for Airflow. Data goes to local folders. dbt compiles; Snowflake optional.
- CI: Lints, tests, validates Terraform, dbt compiles, parses DAGs, builds Docker images.
- Prod: Apply Terraform, connect Airflow to S3 and Snowflake, use GitHub Actions to build/push images.

## Security & IAM
- IAM roles for Airflow and dbt limited by least privilege (S3 read/write to the raw bucket; optional secrets access).
- Snowflake integration service users with scoped roles (`TRANSFORMER`).

## Observability
- Airflow tracks runs; API `/runs` exposes latest DAG runs (backed by metadata DB or local JSON fallback).
- dbt run/test artifacts can be exposed through `/models`.

