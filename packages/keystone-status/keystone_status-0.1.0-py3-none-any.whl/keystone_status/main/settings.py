"""Top level Django application settings."""

import importlib.metadata
import os
import sys
from pathlib import Path

import environ
from django.core.management.utils import get_random_secret_key

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Application metadata

dist = importlib.metadata.distribution('keystone-status')
VERSION = dist.metadata['version']
SUMMARY = dist.metadata['summary']

# Developer settings

env = environ.Env()
DEBUG = env.bool('DEBUG', False)

# Core security settings

SECRET_KEY = os.environ.get('SECURE_SECRET_KEY', get_random_secret_key())
ALLOWED_HOSTS = env.list("SECURE_ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", False)
SECURE_HSTS_PRELOAD = env.bool("SECURE_HSTS_PRELOAD", False)
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", 0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("SECURE_HSTS_SUBDOMAINS", False)

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'apps.cli',
    'apps.api',
    'apps.gui',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    },
]

# Database

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DATABASES = {
    'default': {
        'USER': env.str('DB_USER', ''),
        'PASSWORD': env.str('DB_PASSWORD', ''),
        'HOST': env.str('DB_HOST', 'localhost'),
        'PORT': env.str('DB_PORT', '5432'),
        'timeout': 30,
    }
}

if env.bool('DB_POSTGRES_ENABLE', False):
    DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql'
    DATABASES['default']['NAME'] = env.str('DB_NAME', 'keystone_status')

else:
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3',
    DATABASES['default']['NAME'] = env.str('DB_NAME', BASE_DIR / f'keystone_status.db')

# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticroot"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Timezone

TIME_ZONE = 'UTC'
USE_TZ = True

# Django Rest Framework

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
    'DATETIME_FORMAT': "%b %d %Y, %I:%M %p (%Z)",
}
