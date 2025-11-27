#!/bin/bash
echo "=== Ejecutando migraciones ==="
python manage.py migrate --noinput
echo "=== Migraciones completadas ==="
