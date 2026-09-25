select payment_type_id, payment_type_description from {{ ref('seed_payment_type') }}
