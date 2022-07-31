import json
from uuid import uuid4

from infra.celery import celery_app
from infra.mongodb import get_mongo
from model import Message, Notification

mongodb_client = get_mongo()

CELERY_TASK_CREATE_USER = "distributions.tasks.create_user"
CELERY_TASK_SCHEDULE_NOTIFICATION = "distributions.tasks._schedule_notification"


def callback(ch, method, properties, body):
    message = Message.parse_obj(json.loads(body))

    notification = Notification(
        notification_id=str(uuid4()),
        notification_name=message.notification_name,
        user_id=message.user_id,
        content_id=message.content_id,
        content_value=message.content_value,
        template_id=message.template_id,
    )
    mongodb_client.insert_one(notification.dict())

    notification_data = {
        "id": notification.notification_id,
        "user_id": notification.user_id,
        "template_id": notification.template_id,
    }

    celery_app.send_task(
        CELERY_TASK_SCHEDULE_NOTIFICATION,
        kwargs={"notification_data": notification_data, "periodicity_days": 1},
        countdown=2,
    )
    celery_app.send_task(CELERY_TASK_CREATE_USER, kwargs={"user_id": message.user_id})

    ch.basic_ack(method.delivery_tag)
