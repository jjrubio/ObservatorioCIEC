# -*- coding: utf-8 -*-
"""
Django settings for OSEE project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from .email_info import EMAIL_USE_TLS, EMAIL_HOST, EMAIL_HOST_USER, EMAIL_PORT

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6#6cpmv@i60)wc$-io$=8+n8gh1ifqxfp^06g4^kv_#ql@w4p7'

# SECURITY WARNING: don't run with debug turned on in production!

# DEBUG = False
# TEMPLATE_DEBUG = DEBUG

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

INTERNAL_IPS = ('127.0.0.1',)

GRAPPELLI_ADMIN_HEADLINE = "Observatorio Ecónomico - Social del Ecuador"
GRAPPELLI_ADMIN_TITLE = "Observatorio Ecónomico - Social del Ecuador"

# DEBUG_TOOLBAR_PATCH_SETTINGS = False

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.i18n",
    'django.contrib.messages.context_processors.messages',
)

# Application definition
INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'disintegrations',
    'ENEMDU',
    'features',
    'home',
    'indicators',
    'registers',
    'resources',
    'staff',
    'comercio',
)

MIDDLEWARE_CLASSES = (
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'OSEE.urls'

WSGI_APPLICATION = 'OSEE.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'OESEdb',
        'USER': 'root',
        'PASSWORD': 'jarubandb',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-ES'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

STATIC_URL = '/static/'
STATIC_ROOT = ''

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL='/media/'

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'localhost:6379',#/var/run/redis/redis.sock
        'OPTIONS': {
            'DB': 1,
            'PARSER_CLASS': 'redis.connection.HiredisParser'
        }
    },
}
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

#Email setup
EMAIL_HOST = EMAIL_HOST
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_USE_TLS = EMAIL_USE_TLS
EMAIL_PORT = EMAIL_PORT

#KEY REGISTRATION
AUTH_PROFILE_MODULE = "registers.UserProfile"