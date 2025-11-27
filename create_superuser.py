from django.contrib.auth import get_user_model

User = get_user_model()

USERNAME = "Mrfox"
EMAIL = "Admin@example.com"
PASSWORD = r"7tk3\9)9q>RT"   # r"" para evitar errores por caracteres especiales

if not User.objects.filter(username=USERNAME).exists():
    User.objects.create_superuser(
        username=USERNAME,
        email=EMAIL,
        password=PASSWORD
    )
    print("✔ Superusuario creado correctamente.")
else:
    print("✔ El superusuario ya existe. No se volvió a crear.")
