from django.contrib.auth import get_user_model

User = get_user_model()

USERNAME = "Mrfox"
EMAIL = "admin@example.com"
PASSWORD = r"7tk3\9)9q>RT"

if not User.objects.filter(username=USERNAME).exists():
    user = User.objects.create_superuser(
        username=USERNAME,
        email=EMAIL,
        password=PASSWORD
    )

    # ESTO ES NECESARIO PORQUE TU MODELO LO USA
    user.rol = "admin"
    user.is_admin = True
    user.save()

    print("✔ Superusuario creado correctamente con rol=admin.")
else:
    print("✔ El superusuario ya existe. No se volvió a crear.")
