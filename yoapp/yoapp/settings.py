"""
Django settings for yoapp project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os, sys
from django.contrib import admin

admin.site.site_header = "Halap-YO Admin"
admin.site.site_title = "Halap-YO Admin Portal"
admin.site.index_title = "Welcome to Halap-YO Admin Portal"


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#sys.path.insert(0, os.path.join(BASE_DIR, 'api'))
#sys.path.insert(0, os.path.join(BASE_DIR, 'common'))
#print(BASE_DIR)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jol*#-so3w%w9%n-nti^acl43escr7h46hw*k1pb4)vnn(h4gy'

# admin: s.dusanyuk@gmail.com/admin/adminpassword

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.2.175', 'vivat.sprava.net']
SITE_ID = 1
CORS_ORIGIN_ALLOW_ALL = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_auth.registration',
    'allauth',
    'allauth.account',
    'mptt',
    'django_filters',
    'corsheaders',
    'oauth2_provider',

    # 'social_django',
    # 'rest_social_auth',

    'common.apps.CommonConfig',
    'api.apps.ApiConfig',
    'account.apps.AccountConfig',
    'yomarket.apps.YomarketConfig',
    "push_notifications",
    'django_celery_beat',
    'notification.apps.NotificationConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'rest_framework.authentication.TokenAuthentication',
    'rest_framework.authentication.SessionAuthentication',

    #'social_core.backends.facebook.FacebookOAuth2',
    #'social_core.backends.google.GoogleOAuth2',
]

ROOT_URLCONF = 'yoapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'yoapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
# the root postgre user: postgres/111

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

AUTH_USER_MODEL = 'common.User'

# REST framework definition
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
        'rest_framework.permissions.IsAuthenticated',
        #'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        #'rest_framework.permissions.IsAdminUser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
            #'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
            'rest_framework.authentication.TokenAuthentication',
            #'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
            #'rest_framework.authentication.SessionAuthentication',
            #'rest_framework.authentication.BasicAuthentication',
            #'social_core.backends.facebook.FacebookOAuth2',
            #'social_core.backends.google.GoogleOAuth2',
     ),
    'EXCEPTION_HANDLER': 'api.views.custom_exception_handler',
    #'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    #'PAGE_SIZE': 2
}

#REST_SESSION_LOGIN = False

# ACCOUNT_EMAIL_REQUIRED = False
# ACCOUNT_EMAIL_VERIFICATION = 'none'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# 1234567890qaz - pass for registered test users
# 000 - pass for postgres user on the 192.168.2.175

PUSH_NOTIFICATIONS_SETTINGS = {
    "FCM_API_KEY": "AAAASwElybY:APA91bFaTT_zKLcLYqB0soW8PJmFFG7x1F3wiR0MGta9lLsU22uAVa0VD_3zzz-OremJKDEWEf52OD554byamcwAmZldgrQKfwAjjbhZz_5DYT-z1gcflUBFSWVQQ9lSE9KwDBNHULvfVKmQwxa7xNwuPHz-VfdTbw",
    'USER_MODEL': 'common.User',
    'UPDATE_ON_DUPLICATE_REG_ID':True
}



CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
#CELERY_TIMEZONE = 'Asia/Makassar'
CELERY_BEAT_SCHEDULE = {}