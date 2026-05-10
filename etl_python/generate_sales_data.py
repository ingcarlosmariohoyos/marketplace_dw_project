import pandas as pd
import random
from faker import Faker
import os

# --- CONFIGURACIÓN DE CARPETAS ---
output_dir = os.path.join("data", "raw")
os.makedirs(output_dir, exist_ok=True)

# Semilla para reproducibilidad
Faker.seed(42)
random.seed(42)
fake = Faker()

# 1. GENERAR 5000 ÓRDENES
data_orders = []
for i in range(5000):
    data_orders.append({
        "order_id": i + 1,
        "order_date": fake.date_between(start_date="-1y", end_date="today"),
        "product_id": random.randint(100001, 105000),
        "seller_id": random.randint(1, 1000),
        "customer_id": random.randint(100001, 105000), # Rango compatible con customers
        "units_sold": random.randint(1, 5),
        "price": round(random.uniform(10, 500), 2),
        "discount": round(random.uniform(0, 0.3), 2),
        "shipping_cost": round(random.uniform(5, 30), 2),
        "order_status": random.choice(["pendiente", "enviado", "entregado"]),
        "review_rating": round(random.uniform(1, 5), 1),
    })

df_orders = pd.DataFrame(data_orders)
df_orders.to_csv(os.path.join(output_dir, "amazon_sales.csv"), index=False, encoding='utf-8-sig')

# 2. GENERAR 5000 PRODUCTOS
categories = ["Electrónicos", "Ropa", "Libros", "Hogar y cocina", "Deportes", 
              "Juguetes", "Computadoras", "Salud y cuidado personal", "Automóvil y moto", "Belleza"]

data_products = []
for i in range(5000):
    data_products.append({
        "product_id": 100001 + i,
        "product_name": fake.catch_phrase(),
        "brand": fake.company(),
        "category": random.choice(categories),
        "rating": round(random.uniform(3.5, 5), 1),
        "reviews_count": random.randint(10, 1000),
    })

df_products = pd.DataFrame(data_products)
df_products.to_csv(os.path.join(output_dir, "amazon_products.csv"), index=False, encoding='utf-8-sig')

# 3. GENERAR 5000 CUSTOMERS (NUEVO BLOQUE)
data_customers = []
for i in range(5000):
    data_customers.append({
        "customer_id": 100001 + i,
        "customer_name": fake.name(),
        "email": fake.email(),
        "country": fake.country(),
        "join_date": fake.date_between(start_date="-3y", end_date="-1y").strftime('%Y-%m-%d'),
        "age": random.randint(18, 75)
    })

df_customers = pd.DataFrame(data_customers)
df_customers.to_csv(os.path.join(output_dir, "amazon_customers.csv"), index=False, encoding='utf-8-sig')

print(f"✅ Archivos generados en: {os.path.abspath(output_dir)}")
print("✅ Se crearon 3 archivos: amazon_sales.csv, amazon_products.csv y amazon_customers.csv.")