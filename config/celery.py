from __future__ import absolute_import, unicode_literals
import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('celery_app',
               broker='redis://localhost:6379/0',
               backend='redis://localhost:6379/0'
            )

# default_config = 'config.celeryconfig'
app.config_from_object("django.conf:settings", namespace="CELERY")
# app.config_from_object(default_config)

app.autodiscover_tasks()