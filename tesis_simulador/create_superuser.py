import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# --- CONFIGURAR DJANGO MANUALMENTE ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tesis_simulador.settings")
django.setup()

# Ahora sí se pueden importar modelos
from django.contrib.auth import get_user_model

User = get_user_model()

USERNAME = "Mrfox"
EMAIL = "Admin@example.com"
PASSWORD = r"7tk3\9)9q>RT"

if not User.objects.filter(username=USERNAME).exists():
    User.objects.create_superuser(
        username=USERNAME,
        email=EMAIL,
        password=PASSWORD
    )
    print("✔ Superusuario creado correctamente.")
else:
    print("✔ El superusuario ya existe. No se volvió a crear.")