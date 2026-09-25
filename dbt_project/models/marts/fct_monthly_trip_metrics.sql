-- Gold: monthly metrics by taxi type + borough. DENORMALIZED reporting mart
-- -- joins in human-readable borough names for direct BI consumption.

with trips as (
    select * from {{ ref('fct_trips') }}
),

zones as (
    select * from {{ ref('dim_location') }}
),

trips_with_borough as (
    select
        trips.*,
        zones.borough as pickup_borough
    from trips
    left join zones on trips.pickup_location_id = zones.location_id
)

select
    date_trunc('month', pickup_date)     as trip_month,
    taxi_type,
    pickup_borough,
    count(*)                             as total_trips,
    round(avg(trip_distance), 2)         as avg_trip_distance,
    round(avg(fare_amount), 2)           as avg_fare_amount,
    round(avg(total_amount), 2)          as avg_total_amount,
    round(avg(trip_duration_minutes), 2) as avg_trip_duration_minutes
from trips_with_borough
group by 1, 2, 3
