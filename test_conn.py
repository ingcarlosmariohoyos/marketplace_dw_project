import os
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from dotenv import load_dotenv

# 1. Cargar el archivo .env
load_dotenv()

# 2. Armar la URL
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print("🔄 Intentando conectar a Supabase Pooler...")

try:
    # 3. Crear el engine e intentar una consulta básica
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as connection:
        # Ejecuta un query de control que no toca tablas
        resultado = connection.execute(text("SELECT version();")).fetchone()
        
    print("\n✅ ¡CONEXIÓN EXITOSA DESDE PYTHON!")
    print(f"🖥️ Versión de la BD: {resultado[0]}")

except Exception as e:
    print("\n❌ Error al conectar:")
    print(e)