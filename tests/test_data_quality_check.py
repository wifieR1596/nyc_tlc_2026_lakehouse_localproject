"""
Unit tests for transform/data_quality_check.py.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "transform"))

from data_quality_check import check_no_nulls_in_key_columns, check_positive_values


def test_check_no_nulls_passes_on_clean_data(sample_trips_df):
    assert check_no_nulls_in_key_columns(sample_trips_df, ["pickup_datetime"]) is True


def test_check_positive_values_fails_on_negative_distance(sample_trips_df):
    assert check_positive_values(sample_trips_df, ["trip_distance"]) is False
