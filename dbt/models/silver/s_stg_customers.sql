{{ config(materialized='table') }}

SELECT
    customer_id::int AS customer_id,
    TRIM(customer_name) AS customer_name,
    TRIM(email) AS email,
    UPPER(TRIM(country)) AS country,
    join_date::date AS join_date,
    age::int
FROM {{ source('bronze', 'bronze_customers') }}
WHERE
    customer_id IS NOT NULL
    AND email IS NOT NULL
    AND join_date IS NOT NULL