#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Este comando crea el usuario y nos avisa si funcionó
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); \
if not User.objects.filter(username='admin').exists(): \
    User.objects.create_superuser('admin', 'admin@example.com', 'Josemi2026*'); \
    print('>>> SUPERUSUARIO CREADO: admin / Josemi2026*'); \
else: \
    print('>>> EL SUPERUSUARIO YA EXISTE')"
