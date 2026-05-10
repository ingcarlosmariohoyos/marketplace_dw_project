{{ config(materialized='table') }}

SELECT
    s.order_id,
    TO_CHAR(s.order_date, 'YYYYMMDD')::int AS date_key,
    p.product_key,
    sel.seller_key,
    c.customer_key,
    os.status_key,
    s.units_sold::int,
    s.price::numeric * s.units_sold::int AS order_value,
    s.discount::numeric AS discount_amount,
    s.shipping_cost::numeric,
    s.review_rating::numeric
FROM {{ ref('s_stg_sales') }} s
JOIN {{ ref('dim_product') }} p ON s.product_id = p.product_key
JOIN {{ ref('dim_seller') }} sel ON s.seller_id = sel.seller_key
JOIN {{ ref('dim_customer') }} c ON s.customer_id = c.customer_key
JOIN {{ ref('dim_order_status') }} os ON s.order_status = os.status_name