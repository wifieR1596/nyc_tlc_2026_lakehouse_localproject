-- Gold: fact table, one row per trip (Yellow + Green combined). NORMALIZED --
-- vendor_id/ratecode_id/payment_type/trip_type are foreign keys, described
-- in dim_vendor/dim_ratecode/dim_payment_type/dim_trip_type. Fee columns and
-- store_and_forward_flag are genuine trip-level measures, not codes needing
-- a lookup, so they stay here as-is.

select
    row_number() over(order by pickup_date) as trip_pk,
    taxi_type,
    vendor_id,
    ratecode_id,
    payment_type,
    trip_type,
    store_and_forward_flag,
    pickup_datetime,
    dropoff_datetime,
    datediff('minute', pickup_datetime, dropoff_datetime) as trip_duration_minutes,
    passenger_count,
    trip_distance,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    improvement_surcharge,
    total_amount,
    congestion_surcharge,
    airport_fee,
    cbd_congestion_fee,
    pickup_location_id,
    dropoff_location_id,
    pickup_date,
    {{ dbt_utils.generate_surrogate_key(['taxi_type', 'vendor_id', 'pickup_datetime', 'dropoff_datetime', 'pickup_location_id', 'dropoff_location_id', 'fare_amount', 'trip_distance']) }} as trip_id
from {{ ref('int_trips_unioned') }}
