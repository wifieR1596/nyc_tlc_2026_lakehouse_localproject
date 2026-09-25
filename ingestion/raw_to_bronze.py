from bronze_confiq import INGESTION_CONFIG
from pathlib import Path
import pandas as pd


def run_ingestion():
    for item in INGESTION_CONFIG:
        suffix = Path(item['source']).suffix.lower()
        file = Path(f"{item['bronze']}/{item['bronze_file']}_raw.parquet")

        if file.exists():
            continue

        print(f"Ingesting {item['source_file']}{suffix} to {item['bronze_file']}")

        if suffix == '.parquet':
            df = pd.read_parquet(item['source'])
        elif suffix == '.csv':
            df = pd.read_csv(item['source'])
        else:
            raise ValueError(f"Unsupported file type: {suffix}")

        output = Path(f"{item['bronze']}")
        output.mkdir(parents=True, exist_ok=True)
        df.to_parquet(output / f"{item['bronze_file']}_raw.parquet", index = False)


if __name__ == "__main__":
    run_ingestion()
