{{ config(materialized='table') }}

SELECT
    product_id::int AS product_key,
    product_name,
    brand,
    category,
    rating::numeric(3, 2),
    reviews_count::int
FROM {{ ref('s_stg_products') }}
WHERE product_id IS NOT NULL