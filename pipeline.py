"""
Single entry point that runs the whole pipeline in order:
raw -> bronze -> silver -> gold.

Why this exists: `make` isn't available on Windows by default (only via
WSL or a separate install like Chocolatey), so this is a cross-platform
alternative to the Makefile -- run with `python pipeline.py` from the
project root, works the same on Windows, Mac, or Linux.

Each stage is also runnable on its own (see the Makefile / README for the
individual commands) -- this file just chains them for a one-command run.
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent


def run_ingestion_stage():
    print("\n=== Stage 1/3: raw -> bronze ===")
    sys.path.insert(0, str(PROJECT_ROOT / "ingestion"))
    from raw_to_bronze import run_ingestion
    run_ingestion()


def run_silver_stage():
    print("\n=== Stage 2/3: bronze -> silver ===")
    sys.path.insert(0, str(PROJECT_ROOT / "transform"))
    from bronze_to_silver import transform_bronze_to_silver
    transform_bronze_to_silver()


def run_gold_stage():
    print("\n=== Stage 3/3: silver -> gold (dbt) ===")
    subprocess.run(
        ["dbt", "build"],
        cwd=str(PROJECT_ROOT / "dbt_project"),
        check=True,
    )


if __name__ == "__main__":
    run_ingestion_stage()
    run_silver_stage()
    run_gold_stage()
    print("\nPipeline finished.")
