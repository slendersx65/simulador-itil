import os
import sys

# Agregar la ruta raíz del proyecto al PYTHONPATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar el módulo de settings correctamente
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tesis_simulador.settings")

import django
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

USERNAME = "Mrfox"
EMAIL = "admin@example.com"
PASSWORD = r"7tk3\9)9q>RT"

if not User.objects.filter(username=USERNAME).exists():
    print(">>> Creando superusuario en Railway...")
    User.objects.create_superuser(
        username=USERNAME,
        email=EMAIL,
        password=PASSWORD,
        full_name="Administrador"
    )
    print(">>> Superusuario creado.")
else:
    print("✔ El superusuario ya existe. No se volvió a crear.")
