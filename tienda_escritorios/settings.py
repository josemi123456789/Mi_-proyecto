import os
from pathlib import Path
import dj_database_url  # Importante: para la base de datos en Render

BASE_DIR = Path(__file__).resolve().parent.parent

# CAMBIO 1: ALLOWED_HOSTS para Render
# Reemplaza 'tu-app' por el nombre que le pongas en Render
ALLOWED_HOSTS = ['escritorio.onrender.com', 'localhost', '127.0.0.1']

# CAMBIO 2: Middlewares (Agregar WhiteNoise para archivos estáticos)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Debe ir justo aquí
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CAMBIO 3: Base de Datos dinámica
# Render inyecta la URL de la base de datos automáticamente
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}

# CAMBIO 4: Configuración de Static Files para producción
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Esto permite que Django sirva los archivos comprimidos y con caché
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'