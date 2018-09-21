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

#admin.site.site_header = "Halap-YO Admin"
#admin.site.site_title = "Halap-YO Admin Portal"
#admin.site.index_title = "Welcome to Halap-YO Admin Portal"


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
    'push_notifications',
    'django_celery_beat',
    'django_rest_passwordreset',
    #'rest_framework_tricks',

    'common.apps.CommonConfig',
    'api.apps.ApiConfig',
    'account.apps.AccountConfig',
    'yomarket.apps.YomarketConfig',
    'notification.apps.NotificationConfig',
    'statistic.apps.StatisticConfig',
    'points.apps.PointsConfig',
    'history.apps.HistoryConfig',
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
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'yodb',
        'USER': 'yodbuser',
        'PASSWORD': 'yodbpassword',
        'HOST': '127.0.0.1',
        'PORT': '5432',
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


# 1234567890qaz - pass for registered test users
# 000 - pass for postgres user on the 192.168.2.175


PUSH_NOTIFICATIONS_SETTINGS = {
    "FCM_API_KEY": "AAAAZpeTTNo:APA91bF1IITIT9tZt2BDbjfm44sQ-JqMNsYZAWfq94nSO_7bu3QYTwWE_uwe_gTRQitCKGeGXRRt75dwj-GT0sjKaCVdhAdf31d34gIvZN1T0w2igZonRVawpeDI16TEJ-z87KbahniPvJoGUR1qfJ5FSnwLzGV6aQ",
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
CELERY_WORKER_CONCURRENCY = 1
CELERY_MAX_TASKS_PER_CHILD = 10


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ownerowner346@gmail.com'
DEFAULT_FROM_EMAIL = 'ownerowner346@gmail.com'
EMAIL_HOST_PASSWORD = 'Ownerowner123'
EMAIL_USE_TLS = True

DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME = 1

#admin.site.site_header = 'Halap-YO Admin'
#admin.site.site_title = 'Halap-YO Admin Portal'
#admin.site.index_title = 'Welcome to Halap-YO Admin Portal'