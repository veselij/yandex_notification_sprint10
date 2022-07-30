from celery import Celery
from core.config import BROKER_URL

celery_app = Celery("notification_celery", broker=BROKER_URL)
