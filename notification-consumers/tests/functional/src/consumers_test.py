import json
import os
from tenacity import Retrying, stop_after_delay
from uuid import uuid4

WELCOME_QUEUE = os.getenv("WELCOME_QUEUE", "auth.send-welcome")
UGC_COMMENT_LIKE_QUEUE = os.getenv("UGC_COMMENT_LIKE_QUEUE", "ugc.comment-like")
ADMIN_QUEUE = os.getenv("ADMIN_QUEUE", "admin.send")


def test_admin_consumer(mongodb_client, rabbitmq_client):
    before_count = mongodb_client.notifications.notifications.count_documents({})
    message = {
        "notification_name": "admin_notification",
        "user_id": str(uuid4()),
        "content_id": str(uuid4()),
        "content_value": "content",
    }

    channel = rabbitmq_client.channel()
    channel.basic_publish(exchange='',
                          routing_key=ADMIN_QUEUE,
                          body=json.dumps(message))

    for attempt in Retrying(stop=stop_after_delay(6), reraise=True):
        with attempt:
            count = mongodb_client.notifications.notifications.count_documents({})
            assert (count > before_count) is True

            notification = mongodb_client.notifications.notifications.find_one({"user_id": message["user_id"]})
            assert notification is not None


def test_ugc_like_consumer(mongodb_client, rabbitmq_client):
    before_count = mongodb_client.notifications.notifications.count_documents({})

    message = {
        "notification_name": "new_like",
        "user_id": str(uuid4()),
        "content_id": str(uuid4()),
    }

    channel = rabbitmq_client.channel()
    channel.basic_publish(exchange='',
                          routing_key=ADMIN_QUEUE,
                          body=json.dumps(message))
    for attempt in Retrying(stop=stop_after_delay(6), reraise=True):
        with attempt:
            count = mongodb_client.notifications.notifications.count_documents({})
            assert (count > before_count) is True

            notification = mongodb_client.notifications.notifications.find_one({"user_id": message["user_id"]})
            assert notification is not None


def test_welcome_consumer(mongodb_client, rabbitmq_client, redis_client):
    before_count = mongodb_client.notifications.notifications.count_documents({})

    message = {
        "notification_name": "new_user",
        "user_id": str(uuid4()),
        "content_id": str(uuid4()),
        "content_value": "https://auth.com/",
    }

    channel = rabbitmq_client.channel()
    channel.basic_publish(exchange='',
                          routing_key=WELCOME_QUEUE,
                          body=json.dumps(message))

    for attempt in Retrying(stop=stop_after_delay(6), reraise=True):
        with attempt:
            redis_message = redis_client.lpop('celery', 1)
            assert redis_message is not None

    for attempt in Retrying(stop=stop_after_delay(6), reraise=True):
        with attempt:
            count = mongodb_client.notifications.notifications.count_documents({})
            assert (count > before_count) is True

            notification = mongodb_client.notifications.notifications.find_one({"user_id": message["user_id"]})
            assert notification is not None
