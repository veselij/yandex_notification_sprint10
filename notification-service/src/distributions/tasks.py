from datetime import datetime, timedelta
from typing import Callable, Optional

import pymongo.mongo_client as mongo
from celery import Task, shared_task
from celery.utils.log import get_task_logger
from distributions.services.notification import NotificationClient
from distributions.services.notification.base import (
    DBConnection,
    Notification,
    NotificationResult,
)
from distributions.services.notification.mongo import MongoDBConnection
from distributions.services.sender.base import BaseSender, NotificationChannels
from distributions.services.sender.dummy import DummySender
from distributions.services.sender.email import EmailSender
from distributions.services.template import Template
from distributions.services.userdata import UserDataClient
from distributions.services.userdata.base import UserData
from django.conf import settings
from pymongo.errors import ServerSelectionTimeoutError

logger = get_task_logger(__name__)


class BaseTaskWithRetry(Task):
    autoretry_for = (ServerSelectionTimeoutError,)
    max_retries = 3
    retry_backoff = True
    retry_backoff_max = 700
    retry_jitter = True
    task_ignore_result = True
    task_acks_late = True


class MongoTaskWithRetry(BaseTaskWithRetry):
    _db: Optional[DBConnection] = None

    @property
    def db(self) -> DBConnection:
        if self._db is None:
            client: mongo.MongoClient = mongo.MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
            self._db = MongoDBConnection(client[settings.MONGO_DB][settings.MONGO_COLLECTION])
            logger.info(
                "Connected to MONGO HOST %s PORT %d COLLECTION %s",
                settings.MONGO_HOST,
                settings.MONGO_PORT,
                settings.MONGO_COLLECTION,
            )
        return self._db


@shared_task(base=BaseTaskWithRetry)
def _send_email(user_data: dict, subject: str, body: str, notification_id: str) -> NotificationResult:
    return send(user_data, subject, body, notification_id, EmailSender)


@shared_task(base=BaseTaskWithRetry)
def _send_dummy(user_data: dict, subject: str, body: str, notification_id: str) -> NotificationResult:
    return send(user_data, subject, body, notification_id, DummySender)


@shared_task(base=MongoTaskWithRetry)
def _update_send_status_callback(notification_result: NotificationResult) -> None:
    notification_client = NotificationClient(_update_send_status_callback.db)  # type: ignore
    notification_client.update_notification(notification_result)


notification_tasks_registry: dict[NotificationChannels, Callable]
notification_tasks_registry = {"email": _send_email, "dummy": _send_dummy}


@shared_task(base=MongoTaskWithRetry)
def schedule_notifications(event_name: str, subject: str, periodicity_days: int) -> None:
    notification_client = NotificationClient(schedule_notifications.db)  # type: ignore
    for notification in notification_client.get_notifications(event_name):
        _schedule_notification.delay(notification.dict(), subject, periodicity_days)  # type: ignore


@shared_task(base=BaseTaskWithRetry)
def _schedule_notification(
    notification_data: dict, subject: str, periodicity_days: int, use_timezone: bool = True
) -> None:
    notification = Notification(**notification_data)
    userdata = UserDataClient().get_user_data(notification.user_id)
    tz_adjustment = userdata.timezone if use_timezone else 0
    _get_latest_content.apply_async(
        (notification_data, userdata.dict(), subject, periodicity_days),
        eta=datetime.utcnow() + timedelta(hours=tz_adjustment),
    )  # type: ignore


@shared_task(base=MongoTaskWithRetry)
def _get_latest_content(notification_data: dict, user_data: dict, subject: str, periodicity_days: int):
    notification = Notification(**notification_data)
    userdata = UserData(**user_data)
    notification_client = NotificationClient(_get_latest_content.db)  # type: ignore
    content = notification_client.get_notification_content(notification.id)
    template = Template(notification.template_id)
    body = template.get_content(content["content_value"], userdata.name)
    for task_name, task in notification_tasks_registry.items():
        last_update = content.get(task_name, None)
        if not last_update or datetime.now().timestamp() - last_update > periodicity_days * 24 * 3600:
            task.apply_async(
                (user_data, subject, body, notification.id),
                link=_update_send_status_callback.s(),  # type: ignore
                eta=datetime.utcnow() + timedelta(hours=userdata.timezone),
            )  # type: ignore


def send(
    user_data: dict,
    subject: str,
    body: str,
    notification_id: str,
    sender_cls: type[BaseSender],
) -> NotificationResult:
    userdata = UserData(**user_data)
    sender = sender_cls(userdata)
    sender.send(subject, body)
    return {
        "notification_id": notification_id,
        "notification_channel": sender.notification_channel,
    }
