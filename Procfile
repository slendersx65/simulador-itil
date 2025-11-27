release: python manage.py migrate && python create_superuser.py
web: gunicorn tesis_simulador.wsgi:application
