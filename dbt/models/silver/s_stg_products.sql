{{ config(materialized='table') }}

SELECT
    product_id::int,
    TRIM(product_name) AS product_name,
    TRIM(brand) AS brand,
    LOWER(TRIM(category)) AS category,
    rating::numeric(3, 2),
    reviews_count::int
FROM {{ source('bronze', 'bronze_products') }}
WHERE product_id IS NOT NULL