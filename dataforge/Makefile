PYTHON ?= python3
PIP ?= pip3

.PHONY: bootstrap start test lint format deploy ci dbt-compile airflow-parse

bootstrap:
	@echo "[bootstrap] Creating venv and installing dev deps"
	$(PYTHON) -m venv .venv || true
	. .venv/bin/activate || . .venv/Scripts/activate && \
	  python -m pip install --upgrade pip && \
	  pip install -r api/requirements.txt -r airflow/requirements.txt && \
	  pip install dbt-core dbt-snowflake pre-commit tox sqlfluff flake8 black
	@mkdir -p data/raw data/staging data/logs
	@pre-commit install || true
	@echo "[bootstrap] Initializing Airflow DB (local)"
	AIRFLOW_HOME=airflow . .venv/bin/activate || . .venv/Scripts/activate && airflow db init || true

start:
	docker-compose up --build

lint:
	. .venv/bin/activate || . .venv/Scripts/activate && \
	  black --check api airflow && \
	  flake8 api airflow && \
	  sqlfluff lint dbt

format:
	. .venv/bin/activate || . .venv/Scripts/activate && \
	  black api airflow

test:
	. .venv/bin/activate || . .venv/Scripts/activate && \
	  pytest -q

dbt-compile:
	. .venv/bin/activate || . .venv/Scripts/activate && \
	  dbt --version && dbt compile --project-dir dbt || true

airflow-parse:
	. .venv/bin/activate || . .venv/Scripts/activate && \
	  python -c "import os, importlib.util, glob; dags=glob.glob('airflow/dags/*.py');\
	  [importlib.util.spec_from_file_location(os.path.basename(p)[:-3], p).loader.exec_module(importlib.util.module_from_spec(importlib.util.spec_from_file_location(os.path.basename(p)[:-3], p))) for p in dags];\
	  print('DAG parse ok', len(dags))"

deploy:
	cd infra/terraform && terraform init -input=false && terraform fmt -check && terraform validate && terraform plan -out=tfplan

ci: lint test dbt-compile airflow-parse

