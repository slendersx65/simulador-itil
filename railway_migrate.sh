#!/bin/bash
echo "=== Ejecutando migraciones ==="
python manage.py migrate --noinput

echo "=== Recogiendo archivos estáticos ==="
python manage.py collectstatic --noinput

echo "=== Creando directorio media si no existe ==="
mkdir -p /app/media

echo "=== Todos los comandos completados ==="