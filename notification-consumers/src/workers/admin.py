import json

from infra.celery import celery_app
from model import Message

CELERY_TASK_NAME = "distributions.tasks.create_notifications"


def callback(ch, method, properties, body):
    message = Message.parse_obj(json.loads(body))

    notification_data = {
        "notification_name": message.notification_name,
        "content_id": message.content_id,
        "content_value": message.content_value,
        "template_id": message.template_id,
    }

    celery_app.send_task(
        CELERY_TASK_NAME,
        kwargs=notification_data,
    )
    ch.basic_ack(method.delivery_tag)
