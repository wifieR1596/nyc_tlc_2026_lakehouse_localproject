# Architecture Notes

## Why PySpark for bronze -> silver
2 months x 2 taxi types (4 source files, ~7M+ rows combined for Yellow
alone) is enough volume to justify Spark's distributed processing --
partitioned reads, a real shuffle (dropDuplicates), and a partitioned
write -- while still running on `local[2]` on a laptop (see
`transform/spark_initialize.py` for the memory tuning: driver memory set
to 4g, master capped at 2 threads, both chosen for an 8GB RAM machine
after hitting a real OutOfMemoryError during development).

## Cleaning vs. reconciliation -- the design principle behind the whole pipeline
Two things that look similar are treated differently on purpose:
- **Readability cleanup** (silver's job, in `transform/bronze_to_silver.py`):
  `VendorID` -> `vendor_id`, `PULocationID` -> `pickup_location_id`,
  `RatecodeID` -> `ratecode_id` (with a genuine type cast from double to
  int -- RatecodeID is stored as double in the source file because nulls
  force the whole column to float, even though every real value is a
  whole number), `store_and_fwd_flag` -> `store_and_forward_flag` (also
  cast from Y/N string to a real boolean).
- **Cross-source reconciliation** (dbt's job, in `dbt_project/models/staging/`):
  Yellow's `tpep_pickup_datetime`/`tpep_dropoff_datetime` and Green's
  `lpep_pickup_datetime`/`lpep_dropoff_datetime` are NOT touched in silver
  -- deciding two differently-named columns from different sources mean
  the same thing is a modeling judgment call, not cosmetics, so it's made
  in dbt where it's version-controlled and testable.

## Star schema: normalized fact, denormalized reporting mart
`fct_trips` holds foreign keys (vendor_id, ratecode_id, payment_type,
trip_type) -- descriptions live in `dim_vendor`/`dim_ratecode`/
`dim_payment_type`/`dim_trip_type`, all built from dbt seeds since none of
these lookup tables ship with the actual trip data (unlike
`taxi_zone_lookup.csv`, which does). Fee columns and
`store_and_forward_flag` stay in `fct_trips` since they're genuine
trip-level measures, not codes needing a lookup.

`fct_monthly_trip_metrics` is the intentional exception -- it joins
`dim_location` directly to produce human-readable, BI-ready output, since
it's a reporting mart built for direct consumption rather than the
normalized foundation.