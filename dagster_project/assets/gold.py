import os
import psycopg2
from dagster import asset
from dagster_project.assets.dbt_assets import dbt_assets_def

@asset(deps=[dbt_assets_def], group_name="gold")
def create_foreign_keys():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()

    # Eliminar foreign keys si existen
    cur.execute("ALTER TABLE fact_orders DROP CONSTRAINT IF EXISTS fk_customer;")
    cur.execute("ALTER TABLE fact_orders DROP CONSTRAINT IF EXISTS fk_product;")
    cur.execute("ALTER TABLE fact_orders DROP CONSTRAINT IF EXISTS fk_seller;")
    cur.execute("ALTER TABLE fact_orders DROP CONSTRAINT IF EXISTS fk_time;")
    cur.execute("ALTER TABLE fact_orders DROP CONSTRAINT IF EXISTS fk_status;")

    # Eliminar primary keys si existen
    cur.execute("ALTER TABLE dim_customer DROP CONSTRAINT IF EXISTS pk_customer;")
    cur.execute("ALTER TABLE dim_product DROP CONSTRAINT IF EXISTS pk_product;")
    cur.execute("ALTER TABLE dim_seller DROP CONSTRAINT IF EXISTS pk_seller;")
    cur.execute("ALTER TABLE dim_time DROP CONSTRAINT IF EXISTS pk_time;")
    cur.execute("ALTER TABLE dim_order_status DROP CONSTRAINT IF EXISTS pk_status;")

    # Crear primary keys
    cur.execute("ALTER TABLE dim_customer ADD CONSTRAINT pk_customer PRIMARY KEY (customer_key);")
    cur.execute("ALTER TABLE dim_product ADD CONSTRAINT pk_product PRIMARY KEY (product_key);")
    cur.execute("ALTER TABLE dim_seller ADD CONSTRAINT pk_seller PRIMARY KEY (seller_key);")
    cur.execute("ALTER TABLE dim_time ADD CONSTRAINT pk_time PRIMARY KEY (time_key);")
    cur.execute("ALTER TABLE dim_order_status ADD CONSTRAINT pk_status PRIMARY KEY (status_key);")

    # Crear foreign keys
    cur.execute("ALTER TABLE fact_orders ADD CONSTRAINT fk_customer FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key);")
    cur.execute("ALTER TABLE fact_orders ADD CONSTRAINT fk_product FOREIGN KEY (product_key) REFERENCES dim_product(product_key);")
    cur.execute("ALTER TABLE fact_orders ADD CONSTRAINT fk_seller FOREIGN KEY (seller_key) REFERENCES dim_seller(seller_key);")
    cur.execute("ALTER TABLE fact_orders ADD CONSTRAINT fk_time FOREIGN KEY (date_key) REFERENCES dim_time(time_key);")
    cur.execute("ALTER TABLE fact_orders ADD CONSTRAINT fk_status FOREIGN KEY (status_key) REFERENCES dim_order_status(status_key);")

    conn.commit()
    cur.close()
    conn.close()