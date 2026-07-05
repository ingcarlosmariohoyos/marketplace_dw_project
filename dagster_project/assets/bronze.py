import os
from pathlib import Path
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from dagster import asset

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "raw"

@asset(group_name="bronze")
def create_bronze_tables():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS bronze_orders (
            order_id INTEGER, order_date VARCHAR(20), product_id INTEGER,
            seller_id INTEGER, customer_id INTEGER, units_sold INTEGER,
            price NUMERIC, discount NUMERIC, shipping_cost NUMERIC,
            order_status VARCHAR(20), review_rating NUMERIC
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bronze_products (
            product_id INTEGER, product_name VARCHAR(200), brand VARCHAR(100),
            category VARCHAR(100), rating NUMERIC, reviews_count INTEGER
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bronze_customers (
            customer_id INTEGER, customer_name VARCHAR(200), email VARCHAR(200),
            country VARCHAR(100), join_date VARCHAR(20), age INTEGER
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


@asset(deps=[create_bronze_tables], group_name="bronze")
def load_raw_to_bronze():
    engine = create_engine(
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

    df_sales = pd.read_csv(DATA_DIR / "amazon_sales.csv")
    df_sales.to_sql("bronze_orders", engine, if_exists="replace", index=False)

    df_products = pd.read_csv(DATA_DIR / "amazon_products.csv")
    df_products.to_sql("bronze_products", engine, if_exists="replace", index=False)

    df_customers = pd.read_csv(DATA_DIR / "amazon_customers.csv")
    df_customers.to_sql("bronze_customers", engine, if_exists="replace", index=False)