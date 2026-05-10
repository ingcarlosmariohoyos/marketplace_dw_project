# etl_python/load_raw_to_bronze.py
from sqlalchemy import create_engine
import pandas as pd


engine = create_engine("postgresql://??????:??????@localhost:??????/marketplace_dw")

#Cargar los 5000 ordenes
df_sales = pd.read_csv("../data/raw/amazon_sales.csv")
df_sales.to_sql("bronze_orders", engine, if_exists="replace",index=False)

# Cargar 5000 productos
df_products = pd.read_csv("../data/raw/amazon_products.csv")
df_products.to_sql("bronze_products", engine, if_exists="replace", index=False)

# Cargar 5000 clientes
df_products = pd.read_csv("../data/raw/amazon_customers.csv")
df_products.to_sql("bronze_customers", engine, if_exists="replace", index=False)

print("✅ Datos cargados en Bronze (5000 registros cada uno).")