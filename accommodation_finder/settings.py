import os
from pathlib import Path
import boto3
import json

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET KEY - loaded from AWS Secrets Manager in production
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-secret-key-change-in-production')

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'accommodation_finder.urls'

TEMPLATES = [
    {
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
    },
]

WSGI_APPLICATION = 'accommodation_finder.wsgi.application'

# Database - AWS RDS PostgreSQL in production, SQLite for local dev
def get_db_credentials():
    """Fetch DB credentials from AWS Secrets Manager"""
    secret_name = os.environ.get('DB_SECRET_NAME', '')
    if not secret_name:
        return None
    try:
        client = boto3.client('secretsmanager', region_name=os.environ.get('AWS_REGION', 'eu-west-1'))
        secret = client.get_secret_value(SecretId=secret_name)
        return json.loads(secret['SecretString'])
    except Exception:
        return None

db_credentials = get_db_credentials()

if db_credentials:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': db_credentials.get('dbname', os.environ.get('DB_NAME', 'accommodation_db')),
            'USER': db_credentials.get('username', os.environ.get('DB_USER', 'postgres')),
            'PASSWORD': db_credentials.get('password', os.environ.get('DB_PASSWORD', '')),
            'HOST': db_credentials.get('host', os.environ.get('DB_HOST', 'localhost')),
            'PORT': db_credentials.get('port', os.environ.get('DB_PORT', '5432')),
        }
    }
elif os.environ.get('DB_HOST'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'accommodation_db'),
            'USER': os.environ.get('DB_USER', 'postgres'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'core' / 'static']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# Session settings
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Store sessions in DB
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7   # 7 days in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Keep session after browser closes
SESSION_SAVE_EVERY_REQUEST = True        # Refresh session on every request
SESSION_COOKIE_SECURE = False            # Set True in production (HTTPS)
SESSION_COOKIE_HTTPONLY = True           # Prevent JS access to session cookie
SESSION_COOKIE_SAMESITE = 'Lax'         # CSRF protection

# AWS SES Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'email-smtp.eu-west-1.amazonaws.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('AWS_SES_SMTP_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('AWS_SES_SMTP_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@nestmate.com')
