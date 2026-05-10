{{ config(materialized='table') }}

WITH dates AS (
    SELECT dd::date AS date
    FROM generate_series(
        '2020-01-01'::date,
        '2030-12-31'::date,
        '1 day'::interval
    ) dd
)
SELECT
    TO_CHAR(date, 'YYYYMMDD')::int AS time_key,
    date,
    EXTRACT(YEAR FROM date) AS year,
    EXTRACT(QUARTER FROM date) AS quarter,
    EXTRACT(MONTH FROM date) AS month,
    EXTRACT(DAY FROM date) AS day,
    EXTRACT(DOW FROM date) AS day_of_week,
    TO_CHAR(date, 'Month') AS month_name,
    TO_CHAR(date, 'Day') AS day_name
FROM dates
ORDER BY date