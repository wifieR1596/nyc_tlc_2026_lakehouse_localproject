from pathlib import Path

home_path = (Path(__file__).resolve().parent.parent / "data").as_posix()

INGESTION_CONFIG = [
    #yellow_taxy
    {
        "source_file": "yellow_tripdata_2026-01",
        "source": f"{home_path}/raw/yellow/yellow_tripdata_2026-01.parquet",
        "bronze_file": "yellow_trip_01_2026",
        "bronze": f"{home_path}/bronze"
    },
    {
        "source_file": "yellow_tripdata_2026-02",
        "source": f"{home_path}/raw/yellow/yellow_tripdata_2026-02.parquet",
        "bronze_file": "yellow_trip_02_2026",
        "bronze": f"{home_path}/bronze"
    },
    #green_taxy
    {
        "source_file": "green_tripdata_2026-01",
        "source": f"{home_path}/raw/green/green_tripdata_2026-01.parquet",
        "bronze_file": "green_trip_01_2026",
        "bronze": f"{home_path}/bronze"
    },
    {
        "source_file": "green_tripdata_2026-02",
        "source": f"{home_path}/raw/green/green_tripdata_2026-02.parquet",
        "bronze_file": "green_trip_02_2026",
        "bronze": f"{home_path}/bronze"
    },
    {
        "source_file": "taxi_zone_lookup",
        "source": f"{home_path}/raw/taxi_zone_lookup.csv",
        "bronze_file": "taxi_zone_lookup",
        "bronze": f"{home_path}/bronze"
    }
]
