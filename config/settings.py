


from pathlib import Path
import environ
import os, sys

from datetime import timedelta


from src.fruitshop_app import tasks
from celery.schedules import crontab





# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
# environ.Env.read_env(env_file=os.path.join(BASE_DIR, ".env.dev"))
environ.Env.read_env(env_file=os.path.join(BASE_DIR, ".env"))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/


SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS").split(' ')
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS").split(' ')
# ALLOWED_HOSTS = ['*']
# CSRF_TRUSTED_ORIGINS = ['*']

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
    # "debug_toolbar",
    "django_celery_beat",
]

MIDDLEWARE = [
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
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
        'NAME': env("POSTGRES_DB"),
        'USER': env("POSTGRES_USER"),
        'PASSWORD':env("POSTGRES_PASSWORD"),
        'HOST': env("POSTGRES_HOST"),
        'PORT': env("POSTGRES_PORT"),
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

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# STATIC_URL = 'static/'

STATIC_URL = "/staticfiles/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


ASGI_APPLICATION = "config.asgi.application"

REDIS_HOST = env("REDIS_HOST")


REDIS_URL = env("REDIS_URL")
# CHANNEL_LAYERS = {
    
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [(REDIS_HOST, 6379)],
#             "ssl_cert_reqs": None,
#             # "hosts": [REDIS_URL],
#         },
#     },
# }


CHANNEL_LAYERS = {
    
    "default": {
        # "BACKEND": "channels_redis.core.RedisChannelLayer",
        "BACKEND": "channels_redis.pubsub.RedisPubSubChannelLayer",
        "CONFIG": {
            "hosts":[{
            "address": REDIS_URL,  # "REDIS_TLS_URL"
            # "ssl_cert_reqs": None,
        }]
        },
    },
}


# CELERY_BROKER_URL = "redis://localhost:6379/0"
# CELERY_RESULT_BACKEND = "redis://localhost:6379/1"

# REDIS_URL = env("REDIS_URL")
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

# CELERY_BROKER_URL = f"redis://{REDIS_HOST}:6379"
# CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:6379"


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
    

    "test_second_queuetest_second_queue": {
        "task": "src.fruitshop_app.tasks.test_second_queuetest_second_queue",
        "schedule": timedelta(seconds=2),
    },

    "task_update_account_data_and_last_operations": {
        "task": "src.fruitshop_app.tasks.task_update_account_data_and_last_operations",
        "schedule": timedelta(seconds=10)
    }
}




CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"{REDIS_URL}",
    }
}





