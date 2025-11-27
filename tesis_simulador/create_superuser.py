from django.contrib.auth import get_user_model

User = get_user_model()

USERNAME = "Mrfox"
EMAIL = "admin@example.com"
PASSWORD = r"7tk3\9)9q>RT"

user, created = User.objects.get_or_create(username=USERNAME, defaults={
    "email": EMAIL,
})

user.is_superuser = True
user.is_staff = True
user.is_admin = True
user.rol = "admin"
user.set_password(PASSWORD)
user.save()

print("✔ Superusuario corregido/creado.")