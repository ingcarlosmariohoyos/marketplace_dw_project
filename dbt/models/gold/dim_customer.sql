{{ config(materialized='table') }}

SELECT
    customer_id::int AS customer_key,
    customer_name,
    email,
    country,
    join_date::date,
    age::int
FROM {{ ref('s_stg_customers') }}
WHERE customer_id IS NOT NULL