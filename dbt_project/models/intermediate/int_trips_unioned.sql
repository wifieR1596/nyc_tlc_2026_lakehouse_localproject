-- Intermediate: union Yellow + Green now that staging made their columns agree.

select * from {{ ref('stg_yellow_trips') }}

union all

select * from {{ ref('stg_green_trips') }}
