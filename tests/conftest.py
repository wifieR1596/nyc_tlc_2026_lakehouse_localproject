"""
Pytest fixtures: a small local SparkSession + a tiny sample DataFrame with
one deliberately invalid row, so tests run fast without needing real data.
"""

import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.appName("tests").master("local[1]").getOrCreate()


@pytest.fixture
def sample_trips_df(spark):
    data = [
        (1, "2026-01-01 08:00:00", 2.5, 12.0),
        (2, "2026-01-01 09:00:00", -1.0, 8.0),  # invalid: negative distance, on purpose
    ]
    columns = ["vendor_id", "pickup_datetime", "trip_distance", "fare_amount"]
    return spark.createDataFrame(data, columns)
