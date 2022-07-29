import json
from datetime import datetime
from uuid import uuid4

from infra.mongodb import get_mongo
from model import Message, Notification

mongodb_client = get_mongo()


def mailing_exists(user_id, content_id):
    if mongodb_client.notifications.find_one({"user_id": user_id, "content_id": content_id}):
        return True


def callback(ch, method, properties, body):
    message = Message.parse_obj(json.loads(body))

    if mailing_exists(message.user_id, message.content_id):
        result = mongodb_client.notifications.notifications.update_one({
            "user_id": message.user_id,
            "content_id": message.content_id
        }, {
            "content_value": message.content_value,
            "last_update": datetime.now()
        })
    else:
        notification = Notification(
            notification_id=str(uuid4()),
            notification_name=message.notification_name,
            user_id=message.user_id,
            content_id=message.content_id,
            content_value=message.content_value,
            template_id=message.template_id,
            last_updated=datetime.now()
        )
        result = mongodb_client.notifications.insert_one(notification.dict())

    ch.basic_ack(method.delivery_tag)
