import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Security & Config ---
# Uses terminal variables (like $env:DEBUG="True") if set, otherwise defaults
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-+j2p6l1fkl-6&qc%%4g33eue5e@x6x$v&v!ai88v=3=+o15$v!')
DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 't')

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'skillpoints.adenirantidjani.com']

# --- Application definition ---
INSTALLED_APPS = [
    'core',
    'accounts',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'SkillPoint.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # ADDED: Allows you to put templates in a global folder at the project root
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

WSGI_APPLICATION = 'SkillPoint.wsgi.application'

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

# --- Static Files ---
STATIC_URL = 'static/'
# ADDED: Essential for loading your CSS/JS files
STATICFILES_DIRS = [BASE_DIR / 'static']
# ADDED: Essential for 'python manage.py collectstatic' when you deploy
STATIC_ROOT = BASE_DIR / 'staticfiles'

# --- Redirects ---
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = '/?logout=success'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True