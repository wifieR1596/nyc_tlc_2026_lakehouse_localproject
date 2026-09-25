select ratecode_id, ratecode_description from {{ ref('seed_ratecode') }}
