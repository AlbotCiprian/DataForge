# dataforge — Data Engineering Platform Monorepo

A production‑grade, modular data engineering platform showcasing modern ELT, IaC, orchestration, transformations, warehousing, APIs, and CI/CD. Built to be instructive and extensible.

## Tech Stack
- Python 3.11
- Apache Airflow 2.9+
- dbt-core + dbt-snowflake
- FastAPI + Uvicorn
- Terraform 1.8+
- Docker & docker-compose
- Snowflake (with local fallback for dev)
- pytest + tox
- pre-commit (black, flake8, sqlfluff)

## Architecture (ELT)
```
+-----------+       Extract        +---------+       Load        +-----------+
|  Sources  |  ---------------->   |  Airflow|  --------------> |   S3 Raw  |
+-----------+                       +---------+                  +-----------+
                                                                (Versioned)
                                                                      |
                                                                      v
                                                                +-----------+
                                                                | Snowflake |
                                                                | (dbt)     |
                                                                +-----------+
                                                                      |
                                                                      v
                                                              +---------------+
                                                              |    Marts      |
                                                              |  (dbt models) |
                                                              +---------------+
                                                                      |
                                                                      v
                                                            +------------------+
                                                            |   API (FastAPI)  |
                                                            |  Health/Metadata |
                                                            +------------------+
```

- ELT: Extract/Load to S3 raw, then Transform in Snowflake via dbt.
- Orchestration: Airflow DAGs for ingestion and dbt jobs.
- IaC: Terraform for AWS (S3, IAM) and Snowflake integration users.
- API: FastAPI for health, run metadata, and dbt model introspection.
- CI/CD: Linting, tests, IaC validation, dbt compile, DAG import check, Docker builds.

## Repository Layout
See top-level folders for each subsystem:
- `airflow/` – DAGs, plugins, Airflow image
- `dbt/` – dbt project, models, macros, tests
- `api/` – FastAPI service exposing health/metadata endpoints
- `infra/terraform/` – Terraform root and modules (AWS, Snowflake)
- `scripts/` – bootstrap and helper scripts
- `data/` – local data for dev (raw, staging, logs)
- `.github/workflows/` – CI pipeline

## Quickstart
1) Copy environment file and set credentials
```
cp .env.example .env
```
2) Bootstrap local tooling
```
make bootstrap
```
3) Run tests
```
make test
```
4) Start services
```
docker-compose up --build
```

## Make Targets
- `make bootstrap` – install dev deps, pre-commit, initialize Airflow/dbt
- `make start` – docker-compose up
- `make test` – run lint and tests
- `make deploy` – placeholder for Terraform apply (guarded)

## Conventional Commits
- feat, fix, chore, docs, test, refactor

## Notes
- Snowflake access is optional; dbt can compile without a live warehouse.
- Airflow DAGs are designed to run locally by writing to `data/raw` if S3 is unavailable.

