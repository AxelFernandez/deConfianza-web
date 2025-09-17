from .base import *

# Test environment: debug off but with some development features
DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', 'test.deconfianza.com.ar']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'deconfianza_test'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db-test'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5175",
    "http://127.0.0.1:5175",
    "https://test.deconfianza.com.ar",
]

# Security settings - more strict than dev but less than prod
SECURE_SSL_REDIRECT = False  # No forzar SSL en entorno de pruebas
