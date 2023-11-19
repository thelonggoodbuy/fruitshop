


from pathlib import Path
import environ
import os, sys

from datetime import timedelta


from src.fruitshop_app import tasks
from celery.schedules import crontab





# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(env_file=os.path.join(BASE_DIR, ".env.local"))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/


SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = []

sys.path.insert(0, os.path.join(BASE_DIR, 'src'))


# Application definition

INSTALLED_APPS = [
    'fruitshop_app.apps.FruitShopAppConfig',
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "debug_toolbar",
    # "django_celery_beat",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


INTERNAL_IPS = [
    "127.0.0.1",
]


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env("NAME"),
        'USER': env("USER"),
        'PASSWORD':env("PASSWORD"),
        'HOST': env("HOST"),
        'PORT': env("PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


ASGI_APPLICATION = "config.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}



CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/1"


CELERY_BEAT_SCHEDULE = {
    "task_buy_apple": {
        "task": "src.fruitshop_app.tasks.task_buy_apple",
        "schedule": timedelta(seconds=6),
    },
    "task_buy_banana": {
        "task": "src.fruitshop_app.tasks.task_buy_banana",
        "schedule": timedelta(seconds=9),
    },
    "task_buy_pineapple": {
        "task": "src.fruitshop_app.tasks.task_buy_pineapple",
        "schedule": timedelta(seconds=12),
    },
    "task_buy_peach": {
        "task": "src.fruitshop_app.tasks.task_buy_peach",
        "schedule": timedelta(seconds=15),
    },
    "task_sell_apple": {
        "task": "src.fruitshop_app.tasks.task_sell_apple",
        "schedule": timedelta(seconds=15),
    },
    "task_sell_banana": {
        "task": "src.fruitshop_app.tasks.task_sell_banana",
        "schedule": timedelta(seconds=12),
    },
    "task_sell_pineapple": {
        "task": "src.fruitshop_app.tasks.task_sell_pineapple",
        "schedule": timedelta(seconds=9),
    },
    "task_sell_peach": {
        "task": "src.fruitshop_app.tasks.task_sell_peach",
        "schedule": timedelta(seconds=6),
    },
    

    "task_foo_bar": {
        "task": "src.fruitshop_app.tasks.task_foo_bar",
        "schedule": timedelta(seconds=2),
    },
}




CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
    }
}





