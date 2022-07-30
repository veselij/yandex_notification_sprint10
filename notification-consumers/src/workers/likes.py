import json
from uuid import uuid4

from infra.mongodb import get_mongo
from model import Message, Notification

mongodb_client = get_mongo()


def notification_like_exist(content_id: str, notification_name: str) -> bool:
    if mongodb_client.find_one(
        {"content_id": content_id, "notification_name": notification_name}
    ):
        return True
    return False


def callback(ch, method, properties, body):
    message = Message.parse_obj(json.loads(body))
    if notification_like_exist(message.content_id, message.notification_name):
        mongodb_client.update_one(
            {"user_id": message.user_id, "content_id": message.content_id},
            {"content_value": {"$inc": 1}},
        )
    else:
        notification = Notification(
            notification_id=str(uuid4()),
            notification_name=message.notification_name,
            user_id=message.user_id,
            content_id=message.content_id,
            content_value=1,
            template_id=message.template_id,
        )
        mongodb_client.insert_one(notification.dict())

    ch.basic_ack(method.delivery_tag)
