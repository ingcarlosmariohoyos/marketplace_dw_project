{{ config(materialized='table') }}

WITH statuses AS (
    SELECT 1 AS status_key, 'pendiente'  AS status_name
    UNION ALL
    SELECT 2 AS status_key, 'enviado'    AS status_name
    UNION ALL
    SELECT 3 AS status_key, 'entregado'  AS status_name
    UNION ALL
    SELECT 4 AS status_key, 'cancelado'  AS status_name
)
SELECT
    status_key,
    status_name
FROM statuses