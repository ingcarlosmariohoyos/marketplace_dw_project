{{ config(materialized='table') }}

-- 1. Cargamos tu lista masiva de empresas/vendedores
WITH raw_sellers AS (
    SELECT row_number() OVER (ORDER BY seller_name) as seller_row_id, seller_name
    FROM (
        VALUES 
        ('Abbott-Solis'), ('Abbott-Wallace'), ('Acevedo-Parks'), 
        ('Acevedo, Thompson and Myers'), ('Acosta and Sons'), ('Acosta-Buchanan'),
        ('Acosta-Lopez'), ('Adams-Anderson'), ('Adams and Sons'),
        -- ... aquí puedes pegar el resto de la lista ...
        ('Dixon, Jackson and Jennings'), ('Dodson-Anderson')
    ) AS t(seller_name)
),

-- 2. Lista de países (puedes usar la anterior o una simplificada)
country_list AS (
    SELECT row_number() OVER (ORDER BY country_name) as country_id, country_name
    FROM (
        VALUES 
        ('AFGHANISTAN'), ('ARGENTINA'), ('AUSTRALIA'), ('BRAZIL'), ('CANADA'), 
        ('CHILE'), ('CHINA'), ('COLOMBIA'), ('MEXICO'), ('PERU'), 
        ('SPAIN'), ('UNITED STATES OF AMERICA'), ('VENEZUELA')
    ) AS c(country_name)
)

SELECT DISTINCT
    s.seller_id::int AS seller_key,
    -- Asignamos el nombre de la empresa basándonos en el ID (reparto circular)
    COALESCE(rs.seller_name, 'Empresa Genérica ' || s.seller_id) AS seller_name,
    -- Asignamos el país basándonos en el ID (reparto circular)
    COALESCE(cl.country_name, 'Global') AS country
FROM {{ ref('s_stg_sales') }} s
-- Unión para los nombres de empresas
LEFT JOIN raw_sellers rs 
    ON (s.seller_id % (SELECT COUNT(*) FROM raw_sellers) + 1) = rs.seller_row_id
-- Unión para los países
LEFT JOIN country_list cl 
    ON (s.seller_id % (SELECT COUNT(*) FROM country_list) + 1) = cl.country_id
WHERE s.seller_id IS NOT NULL