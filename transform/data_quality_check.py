"""
Data quality checks on Spark DataFrames, run after bronze -> silver
transformation, before the silver write.
"""

from pyspark.sql import DataFrame
from pyspark.sql.functions import col


def check_no_nulls_in_key_columns(df: DataFrame, key_columns: list[str]) -> bool:
    for c in key_columns:
        null_count = df.filter(col(c).isNull()).count()
        if null_count > 0:
            print(f"Transformation Failed: {null_count} nulls found in {c}")
            return False
    print("Transformation passed: no nulls in key columns")
    return True


def check_positive_values(df: DataFrame, columns: list[str]) -> bool:
    for c in columns:
        negative_count = df.filter(col(c) < 0).count()
        if negative_count > 0:
            print(f"Transformation Failed: {negative_count} negative values in {c}")
            return False
    print("Transformation passed: no negative values")
    return True


def check_row_count_within_range(df: DataFrame, min_rows: int, max_rows: int) -> bool:
    count = df.count()
    passed = min_rows <= count <= max_rows
    print(f"{'PASSED' if passed else 'FAILED'}: row count = {count}")
    return passed
