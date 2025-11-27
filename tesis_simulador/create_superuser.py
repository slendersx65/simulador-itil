import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tesis_simulador.settings")
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