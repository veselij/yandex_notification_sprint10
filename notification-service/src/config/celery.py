import os

from celery import Celery
from config.components import celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("notificaiton_celery")

app.config_from_object(celery)

app.autodiscover_tasks()
