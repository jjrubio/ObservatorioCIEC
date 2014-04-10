# -*- coding: utf-8 -*-
"""
Django settings for OSEE project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6#6cpmv@i60)wc$-io$=8+n8gh1ifqxfp^06g4^kv_#ql@w4p7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.media',
)

GRAPPELLI_ADMIN_TITLE = 'Observatorio Económico - Social del Ecuador'

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
    'procedures',
    'registers',
    'resources',
    'staff',
    'viewers',
    'bootstrap3',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'OSEE.urls'

WSGI_APPLICATION = 'OSEE.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'OSEEdb',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


BOOTSTRAP3 = {
    'jquery_url': '//code.jquery.com/jquery.min.js',
    'base_url': '//netdna.bootstrapcdn.com/bootstrap/3.0.3/',
    'css_url': None,
    'theme_url': None,
    'javascript_url': None,
    'horizontal_label_class': 'col-md-2',
    'horizontal_field_class': 'col-md-4',
}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "media"),
]


STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL='/media/'