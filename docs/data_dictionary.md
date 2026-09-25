# Data Dictionary

## Source: NYC TLC Yellow + Green Taxi Trip Data (2 months each)
- Yellow: https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf
- Green: https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_green.pdf

## Silver Layer -- cleaned per source, NOT merged
- `data/silver/yellow_trips/` -- renamed to common names and change to snake_case, partitioned by pickup_date
- `data/silver/green_trips/` -- renamed to common names and change to snake_case, partitioned by pickup_date
- `data/silver/taxi_zone_lookup/` -- renamed to snake_case

## dbt staging -- reconciliation happens here
- `stg_yellow_trips` / `stg_green_trips` -- renamed to common columns, tagged taxi_type

## dbt intermediate -- union + joins happen here
- `int_trips_unioned` -- UNION ALL of the two staging models

## Gold Layer -- fct_trips, dim_location, fct_monthly_trip_metrics
See `dbt_project/models/marts/_marts__schema.yml`.
