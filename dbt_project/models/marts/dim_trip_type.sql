-- Green-only dimension (street-hail vs dispatch). Yellow trips have
-- trip_type = null and simply won't match a row here in a join.
select trip_type_id, trip_type_description from {{ ref('seed_trip_type') }}
