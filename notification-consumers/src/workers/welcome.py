import json
from datetime import datetime
from uuid import uuid4

from core.config import WELCOME_TEMPLATE_ID
from infra.celery import celery_app
from infra.mongodb import get_mongo
from model import Message, Notification

mongodb_client = get_mongo()

NOTIFICATION_NAME = "new_user"
CELERY_TASK_NAME = "distributions.tasks.schedule_notifications"


def callback(ch, method, properties, body):
    message = Message.parse_obj(json.loads(body))

    notification = Notification(
        notification_id=str(uuid4()),
        notification_name=NOTIFICATION_NAME,
        user_id=message.user_id,
        content_id=message.content_id,
        content_value=message.content_value,
        template_id=WELCOME_TEMPLATE_ID,
        last_updated=datetime.now()
    )
    result = mongodb_client.notifications.insert_one(notification.dict())

    celery_app.send_task(CELERY_TASK_NAME, kwargs={"event_name": NOTIFICATION_NAME, "periodicity_days": 1})

    ch.basic_ack(method.delivery_tag)
