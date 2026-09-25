# NOTE: `make` isn't available on Windows by default (needs WSL or a
# separate install). If you're on Windows without it, use `python
# pipeline.py` instead -- it does the same thing, stage by stage.

.PHONY: ingest silver gold test all

ingest:
	cd ingestion && python raw_to_bronze.py

silver:
	cd transform && python bronze_to_silver.py

gold:
	cd dbt_project && dbt build

test:
	pytest tests/ -v

all: ingest silver gold
