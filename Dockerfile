FROM python:3.11-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema operativo necesarias
# (build-essential y libpq-dev son esenciales para psycopg2, un conector común de PostgreSQL)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias de Python
# Esto se hace primero para aprovechar el cache de Docker si requirements.txt no cambia
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto al directorio de trabajo
COPY . .

# Colectar archivos estáticos de Django (necesario para producción)
RUN python manage.py collectstatic --noinput

# Crear directorio para archivos de media (necesario si tu aplicación usa archivos cargados por usuarios)
RUN mkdir -p /app/media

# Exponer el puerto que usará Gunicorn (8000 por defecto en tu comando)
EXPOSE 8000

# Comando de inicio (entrypoint): 
# 1. Ejecuta las migraciones de la base de datos (migrate)
# 2. Inicia el servidor de producción Gunicorn con el módulo WSGI
CMD sh -c "python manage.py migrate && gunicorn tesis_simulador.wsgi --bind 0.0.0.0:8000"