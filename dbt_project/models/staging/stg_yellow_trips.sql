-- Staging: cross-source reconciliation for Yellow -- unifying tpep_* into
-- the shared pickup_datetime/dropoff_datetime names Green also maps to.
-- trip_type doesn't exist for Yellow, so it's added as a null literal to
-- match Green's column set ahead of the union.

select
    'yellow'                    as taxi_type,
    vendor_id,
    tpep_pickup_datetime        as pickup_datetime,
    tpep_dropoff_datetime       as dropoff_datetime,
    passenger_count,
    trip_distance,
    ratecode_id,
    payment_type,
    cast(null as integer)       as trip_type,
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
    airport_fee,
    cbd_congestion_fee,
    pickup_date
from {{ source('silver', 'yellow_trips') }}
