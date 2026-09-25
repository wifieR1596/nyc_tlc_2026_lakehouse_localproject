from pathlib import Path

home_path = (Path(__file__).resolve().parent.parent / "data").as_posix()

sources = {
    "yellow_taxi": {
        "month_1": f"{home_path}/bronze/yellow_trip_01_2026_raw.parquet",
        "month_2": f"{home_path}/bronze/yellow_trip_02_2026_raw.parquet",
    },
    "green_taxi": {
        "month_1": f"{home_path}/bronze/green_trip_01_2026_raw.parquet",
        "month_2": f"{home_path}/bronze/green_trip_02_2026_raw.parquet",
    },
    "taxi_zone_lookup": f"{home_path}/bronze/taxi_zone_lookup_raw.parquet",
}
