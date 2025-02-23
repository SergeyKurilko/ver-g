"""
Django settings for vertograd project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
from distutils.util import strtobool

# Загрузка переменных из .env
load_dotenv()


from django.conf.global_settings import CSRF_TRUSTED_ORIGINS
from django.contrib.auth.password_validation import MinimumLengthValidator

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '***'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['127.0.0.1', '192.168.100.10', '227kl9-46-22-51-154.ru.tuna.am']
INTERNAL_IPS = ["127.0.0.1"]

ALLOWED_HOSTS = [os.getenv("ALLOWED_HOST_1"), os.getenv("ALLOWED_HOST_2")]

CSRF_TRUSTED_ORIGINS = ['https://227kl9-46-22-51-154.ru.tuna.am', 'http://192.168.100.10:8080']


# YOOKASSA settings
YOOKASSA_SHOP_ID = os.getenv("YOOKASSA_SHOP_ID")
YOOKASSA_SECRET_KEY = os.getenv("YOOKASSA_SECRET_KEY")

# временный для тестов
YOOKASSA_RETURN_URL = 'https://227kl9-46-22-51-154.ru.tuna.am/academy/payment/successful/'

# ver_g_messages_bot
VER_G_MESSAGES_BOT = os.getenv("VER_G_MESSAGES_BOT")

# Чаты для оповещений ботом telegram
# Чат с комментариями оставленными в блоге и в шагах
COMMENTS_FROM_VER_G_CHAT_ID = os.getenv("COMMENTS_FROM_VER_G_CHAT_ID")
# Чат для работы с админкой и БД
ADMIN_VER_G_CHAT_ID = os.getenv("ADMIN_VER_G_CHAT_ID")
# Оповещения об активностях на ver-g/academy
EDUCATION_PLATFORM_ACTIVITY_CHAT_ID = os.getenv("EDUCATION_PLATFORM_ACTIVITY_CHAT_ID")
# Заявки из форм на ver-g
FORMS_AT_VER_G_CHAT_ID = os.getenv("FORMS_AT_VER_G_CHAT_ID")

# TELEGRAM ADMIN CHATS SETTINGS
# sergey_chat and elena_chat
VER_G_ADMIN_TELEGRAM_CHAT_IDS = [os.getenv("ELENA_CHAT_ID"), os.getenv("SERGEY_CHAT_ID")]

# API KEY
API_KEY_VER_G = os.getenv("API_KEY_VER_G")

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
#             'style': '{',
#         },
#         'simple': {
#             'format': '{levelname} {message}',
#             'style': '{',
#         },
#     },
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': os.path.join(BASE_DIR, 'logs/ver_g_log.log'),
#             'formatter': 'verbose',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'INFO',  # Установите уровень на INFO, чтобы не логировать SQL-запросы
#             'propagate': True,
#         },
#         'api': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'widget_tweaks',
    'easy_thumbnails',
    'ckeditor',
    'ckeditor_uploader',
    'nested_admin',
    'django_extensions',
    'blog.apps.BlogConfig',
    'education.apps.EducationConfig',
    'order.apps.OrderConfig',
    'portfolio.apps.PortfolioConfig',
    'service.apps.ServiceConfig',
    'reviews.apps.ReviewsConfig',
    'comments.apps.CommentsConfig',
    'education_platform.apps.EducationPlatformConfig',
    'django.contrib.humanize',
    "debug_toolbar",
    "api"
]


SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        }
    }
}



ROOT_URLCONF = 'vertograd.urls'

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
                'vertograd.context_processor.get_context_data'
            ],
        },
    },
]

WSGI_APPLICATION = 'vertograd.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DATA_UPLOAD_MAX_NUMBER_FIELDS = 2500


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'education_platform.backends.EmailBackend'
]


LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


THUMBNAIL_ALIASES = {
    '': {
        'article_image_preview': {'size': (180, 180), 'crop': True},
        'logo_image_preview': {'size': (50, 50), 'crop': True},
    },
}


CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': 700,
        'stylesSet': [
            {
                "name": 'зеленый блок',
                "element": 'div',
                "attributes": {'class': 'green-back'},
            },
            {
                "name": 'зеленый блок в центре',
                "element": 'div',
                "attributes": {'class': 'green-back-center'},
            },
            {
                "name": 'зеленый блок c градиентом',
                "element": 'div',
                "attributes": {'class': 'green-back-gradient'},
            },
            {
                "name": 'зеленый блок в центре c градиентом',
                "element": 'div',
                "attributes": {'class': 'green-back-center-gradient'},
            },
            {
                "name": 'сделать фото 2 к 1 в центре с фоном',
                "element": 'div',
                "attributes": {'class': 'two-to-one-center-with-back sm'}
            }
        ],
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# zakaz@ver-g.ru and no-reply@ver-g.ru settings
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_SSL = strtobool(os.getenv("EMAIL_USE_SSL"))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = strtobool(os.getenv("EMAIL_USE_TLS"))
NO_REPLY_DEFAULT_FROM_EMAIL = os.getenv("NO_REPLY_DEFAULT_FROM_EMAIL")


REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'



