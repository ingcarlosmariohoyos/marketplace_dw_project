import psycopg2
from psycopg2 import sql

#parametros de conexion
HOST = "localhost"
DATABASE = "marketplace_dw"
USER = "*******"
PASSWORD = "*****"
PORT = "****"

#Conectar a postgresql
conn = psycopg2.connect(
    host=HOST,
    database=DATABASE,
    user=USER,
    password=PASSWORD,
    port=PORT
)
cur = conn.cursor()

# Crear tabla de bronze_orders
cur.execute("""
        CREATE TABLE IF NOT EXISTS bronze_orders (
        order_id INTEGER,
        order_date VARCHAR(20),
        product_id INTEGER,
        seller_id INTEGER,
        customer_id INTEGER,
        units_sold INTEGER,
        price NUMERIC,
        discount NUMERIC,
        shipping_cost NUMERIC,
        order_status VARCHAR(20),
        review_rating NUMERIC
    );
""")

# Crear tabla bronze_products
cur.execute("""
    CREATE TABLE IF NOT EXISTS bronze_products (
        product_id INTEGER,
        product_name VARCHAR(200),
        brand VARCHAR(100),
        category VARCHAR(100),
        rating NUMERIC,
        reviews_count INTEGER
    );
""")

# Crear tabla bronze_customers
cur.execute("""
    CREATE TABLE IF NOT EXISTS bronze_customers (
        customer_id INTEGER,
        customer_name VARCHAR(200),
        email VARCHAR(200),
        country VARCHAR(100),
        join_date VARCHAR(20),
        age INTEGER
    );
""")

#confirmar cambios
conn.commit()

#mostrar las tablas creadas
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")

tables = cur.fetchall()
print("Tablas en 'public':")
for table in tables:
    print(f"  - {table[0]}")

# Cerrar conexión
cur.close()
conn.close()

"""prueba de conexion
try:
    # 1. Intentar la conexión
    connection = psycopg2.connect(
        host=HOST,
        database=DATABASE,
        user=USER,
        password=PASSWORD,
        port=PORT
    )

    # 2. Crear un cursor para ejecutar una consulta simple
    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()

    print("¡Conexión exitosa!")
    print(f"Estás conectado a: {db_version}")

    # 3. Cerrar sesión
    cursor.close()
    connection.close()
    print("Conexión cerrada correctamente.")

except Exception as error:
    print(f"Error al conectar a la base de datos: {error}")
    """