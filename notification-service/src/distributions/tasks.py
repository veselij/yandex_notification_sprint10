import uuid
from datetime import datetime, timedelta

from celery import shared_task
from celery.utils.log import get_task_logger
from distributions.models import AuthUser
from distributions.services.exceptions import NoUserDataExceptionError
from distributions.services.notification.base import (
    Notification,
    NotificationClient,
    NotificationResult,
)
from distributions.services.userdata import UserDataClient
from distributions.tasks_base import (
    BaseTaskWithRetry,
    MongoTaskWithRetry,
    RequestsTaskRetry,
)
from distributions.tasks_channels import notification_tasks_registry

logger = get_task_logger(__name__)


@shared_task(base=MongoTaskWithRetry)
def schedule_notifications(
    event_name: str, periodicity_days: int, use_timezone: bool = True
) -> None:
    notification_client = NotificationClient(schedule_notifications.db)  # type: ignore
    for notification in notification_client.get_notifications(event_name):
        _schedule_notification.delay(notification.dict(), periodicity_days, use_timezone)  # type: ignore


@shared_task(base=RequestsTaskRetry)
def _schedule_notification(
    notification_data: dict,
    periodicity_days: int,
    use_timezone: bool = True,
) -> None:
    notification = Notification(**notification_data)
    user_client = UserDataClient()
    try:
        userdata = user_client.get_user_data(notification.user_id)
    except NoUserDataExceptionError as e:
        logger.exception(e)
    else:
        tz_adjustment = userdata.timezone if use_timezone else 0
        logger.debug("user timezone %d", tz_adjustment)
        logger.debug("notificaition data %s", userdata.json())
        _get_latest_content.apply_async(
            (notification_data, userdata.dict(), periodicity_days),
            eta=datetime.utcnow() + timedelta(hours=tz_adjustment),
        )  # type: ignore


@shared_task(base=MongoTaskWithRetry)
def _get_latest_content(
    notification_data: dict, user_data: dict, periodicity_days: int
) -> None:
    notification = Notification(**notification_data)
    notification_client = NotificationClient(_get_latest_content.db)  # type: ignore
    content = notification_client.get_notification_content(notification.id)
    logger.debug("notification content %s", content)
    for task_name, task in notification_tasks_registry.items():
        last_update = content.get(task_name, None)
        if (
            not last_update
            or datetime.now().timestamp() - last_update > periodicity_days * 24 * 3600
        ):
            task.apply_async(  # type: ignore
                (user_data, notification_data, content["content_value"]),
                link=_update_send_status_callback.s(),  # type: ignore
            )  # type: ignore


@shared_task(base=MongoTaskWithRetry)
def _update_send_status_callback(notification_result: NotificationResult) -> None:
    notification_client = NotificationClient(_update_send_status_callback.db)  # type: ignore
    notification_client.update_notification(notification_result)


@shared_task(base=BaseTaskWithRetry)
def create_user(user_id: str) -> None:
    AuthUser.objects.get_or_create(auth_user_id=user_id)


@shared_task(base=MongoTaskWithRetry)
def create_notifications(
    notification_name: str, content_id: str, content_value: str, template_id: str
):
    notification_client = NotificationClient(create_notifications.db)  # type: ignore
    for user in AuthUser.objects.all():
        notification_id = str(uuid.uuid4())
        notification_client.insert_or_update_notification(
            str(user.auth_user_id),
            notification_id,
            notification_name,
            content_id,
            content_value,
            template_id,
        )
