{{ config(materialized='table') }}

SELECT
    order_id,
    order_date::date AS order_date,
    product_id::int,
    seller_id::int,
    customer_id::int,
    units_sold::int,
    price::numeric(10, 2),
    COALESCE(discount, 0) AS discount,
    COALESCE(shipping_cost, 0) AS shipping_cost,
    LOWER(TRIM(order_status)) AS order_status,
    review_rating::numeric(2, 1) AS review_rating
FROM {{ source('bronze', 'bronze_orders') }}
WHERE
    order_date IS NOT NULL
    AND price > 0
    AND units_sold > 0