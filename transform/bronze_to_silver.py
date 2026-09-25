from data_quality_check import check_no_nulls_in_key_columns, check_positive_values
from pyspark.sql.functions import col, to_date, trim, upper, when
from utils.schemas import yellow_trips_schema, green_trips_schema, taxi_zone_schema
from silver_confiq import sources
from utils.spark_initialize import get_spark_session
from pathlib import Path

home_path = (Path(__file__).resolve().parent.parent / "data").as_posix()

def clean_yellow(spark):
    df = (
        spark.read.schema(yellow_trips_schema).parquet(*sources["yellow_taxi"].values())
        .drop_duplicates()
        .filter(col("trip_distance") > 0)
        .filter(col("total_amount") >= 0)
        .filter(col("fare_amount") >= 0)
        .filter(col("tpep_pickup_datetime").isNotNull())
        .filter(col("tpep_dropoff_datetime").isNotNull())
        .withColumn("pickup_date", to_date(col("tpep_pickup_datetime")))
        .withColumn("store_and_fwd_flag",
                     when(trim(upper(col("store_and_fwd_flag"))) == "Y", True)
                    .when(trim(upper(col("store_and_fwd_flag"))) == "N", False)
                    .otherwise(None))
        .withColumn("passenger_count", col("passenger_count").cast("int"))
        .withColumn("RatecodeID", col("RatecodeID").cast("int"))
        .withColumn("payment_type", col("payment_type").cast("int"))
        .withColumnRenamed("VendorID", "vendor_id")
        .withColumnRenamed("RatecodeID", "ratecode_id")
        .withColumnRenamed("store_and_fwd_flag", "store_and_forward_flag")
        .withColumnRenamed("PULocationID", "pickup_location_id")
        .withColumnRenamed("DOLocationID", "dropoff_location_id")
        .withColumnRenamed("Airport_fee", "airport_fee")
    )
    assert check_no_nulls_in_key_columns(df, ["tpep_pickup_datetime", "tpep_dropoff_datetime"])
    assert check_positive_values(df, ["trip_distance", "fare_amount"])
    return df

def clean_green(spark):
    df = (
        spark.read.schema(green_trips_schema).parquet(*sources["green_taxi"].values())
        .drop_duplicates()
        .filter(col("trip_distance") > 0)
        .filter(col("total_amount") >= 0)
        .filter(col("fare_amount") >= 0)
        .filter(col("lpep_pickup_datetime").isNotNull())
        .filter(col("lpep_dropoff_datetime").isNotNull())
        .withColumn("pickup_date", to_date(col("lpep_pickup_datetime")))
        .withColumn("store_and_fwd_flag",
                     when(trim(upper(col("store_and_fwd_flag"))) == "Y", True)
                    .when(trim(upper(col("store_and_fwd_flag"))) == "N", False)
                    .otherwise(None))
        .withColumn("passenger_count", col("passenger_count").cast("int"))
        .withColumn("RatecodeID", col("RatecodeID").cast("int"))
        .withColumn("payment_type", col("payment_type").cast("int"))
        .withColumn("trip_type", col("trip_type").cast("int"))
        .withColumnRenamed("VendorID", "vendor_id")
        .withColumnRenamed("RatecodeID", "ratecode_id")
        .withColumnRenamed("store_and_fwd_flag", "store_and_forward_flag")
        .withColumnRenamed("PULocationID", "pickup_location_id")
        .withColumnRenamed("DOLocationID", "dropoff_location_id")
    )
    assert check_no_nulls_in_key_columns(df, ["lpep_pickup_datetime", "lpep_dropoff_datetime"])
    assert check_positive_values(df, ["trip_distance", "fare_amount"])
    return df

def clean_zones(spark):
    df = (
        spark.read.schema(taxi_zone_schema).parquet(sources["taxi_zone_lookup"])
        .withColumnRenamed("LocationID", "location_id")
        .withColumnRenamed("Borough", "borough")
        .withColumnRenamed("Zone", "zone")
    )
    return df

def silver_write_complete(path: str) -> bool:
    #checking if spark write is completed and success
    return (Path(path) / "_SUCCESS").exists()

def transform_bronze_to_silver(force: bool = False) -> None:
    silver_yellow_path = f"{home_path}/silver/yellow_trips"
    silver_green_path = f"{home_path}/silver/green_trips"
    silver_zones_path = f"{home_path}/silver/taxi_zone_lookup"

    #this code check that silver output is already there in previous run and successfull, so doesn't need to rerun spark jobs again"
    if not force and all(
        silver_write_complete(p) for p in [silver_yellow_path, silver_green_path, silver_zones_path]
    ):
        print("Silver output already exists and completed successfully, skipping. Pass force=True to re-run.")
        return

    spark = get_spark_session()

    yellow = clean_yellow(spark)
    green = clean_green(spark)
    zones = clean_zones(spark)

    print(f"silver yellow_trips: {yellow.count()} rows")
    print(f"silver green_trips: {green.count()} rows")

    yellow.write.mode("overwrite").partitionBy("pickup_date").parquet(f"{home_path}/silver/yellow_trips/")
    green.write.mode("overwrite").partitionBy("pickup_date").parquet(f"{home_path}/silver/green_trips/")
    zones.write.mode("overwrite").parquet(f"{home_path}/silver/taxi_zone_lookup/")

    spark.stop()

if __name__ == "__main__":
    transform_bronze_to_silver()
