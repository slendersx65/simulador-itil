#!/bin/bash
echo "=== Creando superusuario en Railway ==="
python manage.py shell < create_superuser.py
echo "=== Superusuario listo ==="
