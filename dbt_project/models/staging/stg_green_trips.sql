-- Staging: same reconciliation for Green -- lpep_* -> shared pickup/dropoff
-- names. airport_fee doesn't exist for Green (not a real fee TLC charges
-- for green taxis), so it's added as a null literal to match Yellow's
-- column set ahead of the union.

select
    'green'                     as taxi_type,
    vendor_id,
    lpep_pickup_datetime        as pickup_datetime,
    lpep_dropoff_datetime       as dropoff_datetime,
    passenger_count,
    trip_distance,
    ratecode_id,
    payment_type,
    trip_type,
    store_and_forward_flag,
    pickup_location_id,
    dropoff_location_id,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    improvement_surcharge,
    total_amount,
    congestion_surcharge,
    cast(null as double)        as airport_fee,
    cbd_congestion_fee,
    pickup_date
from {{ source('silver', 'green_trips') }}
