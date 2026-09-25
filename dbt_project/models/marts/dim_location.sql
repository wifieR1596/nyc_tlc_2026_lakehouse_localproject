select
    location_id,
    borough,
    zone,
    service_zone
from {{ ref('stg_taxi_zones') }}
