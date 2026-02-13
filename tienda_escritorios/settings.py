import os
from pathlib import Path
import dj_database_url  # Ya se instala correctamente según tus logs

BASE_DIR = Path(__file__).resolve().parent.parent

# SEGURIDAD: Mantén esto en secreto
SECRET_KEY = 'django-insecure-%@vk8!bz+nei5o_j&v0a5@_ws4yq-qb$j4zis5*g$3*u-=9h!e'

# DEBUG: En Render debe ser False
DEBUG = False

# CAMBIO 1: Ajustado a tu URL real de Render que vi en tu captura
ALLOWED_HOSTS = ['mi-proyecto-2dqb.onrender.com', 'localhost', '127.0.0.1']

# CAMBIO 2: ¡ESTO ES LO QUE FALTABA! Por eso fallaba el collectstatic
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', # Esta línea activa el comando collectstatic
    'store', # Tu aplicación de la tienda
]

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

ROOT_URLCONF = 'tienda_escritorios.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tienda_escritorios.wsgi.application'

# CAMBIO 3: Base de Datos dinámica para Render
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}

# Configuración de archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Almacenamiento optimizado para WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Configuración regional (Ecuador)
LANGUAGE_CODE = 'es-ec'
TIME_ZONE = 'America/Guayaquil'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CSRF para que funcionen los formularios en Render
CSRF_TRUSTED_ORIGINS = [
    'https://mi-proyecto-2dqb.onrender.com',
]

# Configuración de Stripe (Tus llaves de prueba)
STRIPE_PUBLIC_KEY = 'pk_test_51T0BOwDJanrHiNNXugT1ePbgk62SRwTzOGNNn0P2l2WJZ2dgrUqR25sXv9WTyxuuNG7Iafl4pC6VlwyCl1qo27q400dauib5U6'
STRIPE_SECRET_KEY = 'sk_test_51T0BOwDJanrHiNNX6qEERc5erNuyFYO34SLTaqckriS2kkMh392A8gwhTak3HZoUbwk2aeAK4oJOa0tlwymhRI6Z00gCuB0piR'
