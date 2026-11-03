"""Configuración de Django: MySQL local y MySQL alojado en Railway."""
from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

# Nunca publicar claves reales en GitHub. Cambiar al desplegar.
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'solo-desarrollo-local-cambiar-antes-de-publicar-2026')
DEBUG = os.getenv('DJANGO_DEBUG', '1') == '1'
ALLOWED_HOSTS = [host.strip() for host in os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',') if host.strip()]
CSRF_TRUSTED_ORIGINS = [url.strip() for url in os.getenv('DJANGO_CSRF_TRUSTED_ORIGINS', '').split(',') if url.strip()]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'clientes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_clientes.urls'
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]
WSGI_APPLICATION = 'django_clientes.wsgi.application'
ASGI_APPLICATION = 'django_clientes.asgi.application'

# En el laboratorio, MySQL es la base principal. SQLite solo se ofrece para
# pruebas automáticas de código si aún no hay servidor MySQL disponible.
if os.getenv('DB_ENGINE', 'mysql').lower() == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME', os.getenv('MYSQLDATABASE', 'django_db')),
            'USER': os.getenv('DB_USER', os.getenv('MYSQLUSER', 'root')),
            'PASSWORD': os.getenv('DB_PASSWORD', os.getenv('MYSQLPASSWORD', '')),
            'HOST': os.getenv('DB_HOST', os.getenv('MYSQLHOST', '127.0.0.1')),
            'PORT': os.getenv('DB_PORT', os.getenv('MYSQLPORT', '3306')),
            'OPTIONS': {'charset': 'utf8mb4'},
            'CONN_MAX_AGE': 60,
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Guatemala'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'

# Para replicar la guía se usa correo de consola. Para enviar correos reales,
# configurar SMTP_EMAIL_* y SMTP_HOST en .env / variables Railway.
if os.getenv('SMTP_HOST'):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ['SMTP_HOST']
    EMAIL_PORT = int(os.getenv('SMTP_PORT', '587'))
    EMAIL_USE_TLS = os.getenv('SMTP_USE_TLS', '1') == '1'
    EMAIL_HOST_USER = os.getenv('SMTP_USER', '')
    EMAIL_HOST_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    DEFAULT_FROM_EMAIL = os.getenv('SMTP_FROM', EMAIL_HOST_USER)
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Railway termina HTTPS en su proxy. Esto permite que Django lo reconozca.
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
