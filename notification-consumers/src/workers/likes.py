import json
from datetime import datetime
from uuid import uuid4

from core.config import UGC_COMMENT_LIKE_TEMPLATE_ID
from infra.mongodb import get_mongo
from model import Message, Notification

mongodb_client = get_mongo()

NOTIFICATION_NAME = "new_likes"


def notification_like_exist(content_id):
    if mongodb_client.notifications.find_one({"content_id": content_id, "notification_name": NOTIFICATION_NAME}):
        return True


def callback(ch, method, properties, body):
    message = Message.parse_obj(json.loads(body))
    if notification_like_exist(message.content_id):
        result = mongodb_client.notifications.notifications.update_one({
            "user_id": message.user_id,
            "content_id": message.content_id
        }, {
            "content_value": {"$inc": 1},
            "last_update": datetime.now()
        })
    else:
        notification = Notification(
            notification_id=str(uuid4()),
            notification_name=NOTIFICATION_NAME,
            user_id=message.user_id,
            content_id=message.content_id,
            content_value=1,
            template_id=UGC_COMMENT_LIKE_TEMPLATE_ID,
            last_updated=datetime.now()
        )
        result = mongodb_client.notifications.notifications.insert_one(notification.dict())

    ch.basic_ack(method.delivery_tag)
