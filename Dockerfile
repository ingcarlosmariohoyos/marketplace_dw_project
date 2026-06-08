# 1. Usamos una imagen oficial de Python ligera basada en Debian
FROM python:3.11-slim

# 2. Instalar dependencias del sistema necesarias para compilar PostgreSQL y dbt
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# 3. Definir el directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Copiar los archivos de requerimientos primero (optimiza la caché de Docker)
COPY requirements.txt .

# 5. Crear el entorno virtual exacto e instalar las dependencias
RUN python -m venv dbt_env_39
RUN ./dbt_env_39/bin/pip install --no-cache-dir --upgrade pip && \
    ./dbt_env_39/bin/pip install --no-cache-dir -r requirements.txt

# 6. Copiar el resto del código del proyecto al contenedor
COPY . .

# 7. Exponer el puerto 3000 que es el que usa la interfaz de Dagster
EXPOSE 3000

# 8. Comando por defecto: Activa el entorno virtual y arranca Dagster en modo producción
# Escucha en 0.0.0.0 para que plataformas como Render puedan redirigir el tráfico web
CMD ["./dbt_env_39/bin/dagster", "dev", "-h", "0.0.0.0", "-p", "3000", "-f", "dagster_project/definitions.py"]