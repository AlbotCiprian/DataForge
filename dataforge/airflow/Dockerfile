FROM apache/airflow:2.9.1-python3.11

USER root
RUN mkdir -p /opt/data && chown -R airflow:airflow /opt/data
USER airflow

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY dags/ /opt/airflow/dags/
COPY plugins/ /opt/airflow/plugins/

ENV AIRFLOW__CORE__LOAD_EXAMPLES=False

