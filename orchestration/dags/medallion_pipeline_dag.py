"""
Reference Airflow DAG for the NYC TLC medallion pipeline.

NOT currently run -- Airflow doesn't run natively on Windows (needs WSL2
or Docker), so this is written and ready, but kept as a portfolio
reference / something to actually run later once you set up WSL2/Docker
for Airflow, rather than something wired into your day-to-day workflow now.

Design note: each task shells out to run the exact same command the
Makefile / pipeline.py already use (`python raw_to_bronze.py`, `python
bronze_to_silver.py`, `dbt build`), rather than importing your ingestion/
transform functions directly into the Airflow process. This is
deliberate: your scripts use flat imports (e.g. `from bronze_confiq
import ...`) that rely on their own folder being on sys.path when run
directly -- running each script as its own subprocess sidesteps any
import-path fragility that could come from Airflow's process having a
different working directory or sys.path than a normal terminal run.

To actually use this: set PROJECT_ROOT to wherever this repo lives on
the machine running Airflow, and place (or symlink) this file into your
Airflow DAGs folder (usually $AIRFLOW_HOME/dags).
"""

from datetime import datetime
from pathlib import Path
import subprocess

from airflow.decorators import dag, task

# TODO: set this to the actual path of this project on the machine
# running Airflow (e.g. inside WSL2: "/mnt/c/Data Irhas/Career Switch/project_files/nyc-tlc-2026-lakehouse-project")
PROJECT_ROOT = Path("/path/to/nyc-tlc-2026-lakehouse-project")


@dag(
    dag_id="nyc_tlc_medallion_pipeline",
    description="Raw -> bronze -> silver -> gold for NYC TLC taxi trip data",
    schedule=None,  # manual trigger -- this is a one-time full load, not a recurring job
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["portfolio", "medallion", "nyc-tlc"],
)
def nyc_tlc_medallion_pipeline():

    @task
    def ingest_raw_to_bronze():
        subprocess.run(
            ["python", "raw_to_bronze.py"],
            cwd=str(PROJECT_ROOT / "ingestion"),
            check=True,
        )

    @task
    def transform_bronze_to_silver():
        subprocess.run(
            ["python", "bronze_to_silver.py"],
            cwd=str(PROJECT_ROOT / "transform"),
            check=True,
        )

    @task
    def build_gold_layer():
        subprocess.run(
            ["dbt", "seed"],
            cwd=str(PROJECT_ROOT / "dbt_project"),
            check=True,
        )
        subprocess.run(
            ["dbt", "build"],
            cwd=str(PROJECT_ROOT / "dbt_project"),
            check=True,
        )

    # Task dependencies: bronze must finish before silver, silver before gold.
    # TaskFlow API infers this automatically from call order when tasks are
    # chained like this, but writing it explicitly with >> is clearer to read.
    ingest_raw_to_bronze() >> transform_bronze_to_silver() >> build_gold_layer()


nyc_tlc_medallion_pipeline()
