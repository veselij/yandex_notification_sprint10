from typing import Callable

from celery import shared_task
from distributions.services.notification.base import Notification, NotificationResult
from distributions.services.sender import EmailSender
from distributions.services.sender.base import BaseSender, NotificationChannels
from distributions.services.template.base import BaseTemplate
from distributions.services.template.jinja import JinjaTemplate
from distributions.services.userdata.base import UserData
from distributions.tasks_base import SendTaskRetry


@shared_task(base=SendTaskRetry)
def send_email(
    user_data: dict, notification_data: dict, content_value: str
) -> NotificationResult:
    notification = Notification(**notification_data)
    template = JinjaTemplate(notification.template_id, "email")
    return send(user_data, template, notification.id, EmailSender, content_value)


def send(
    user_data: dict,
    template: BaseTemplate,
    notification_id: str,
    sender_cls: type[BaseSender],
    content_value: str,
) -> NotificationResult:
    userdata = UserData(**user_data)
    body = template.get_content(content_value, userdata)
    sender = sender_cls(userdata)
    sender.send(template.get_subject(), body)
    return {
        "notification_id": notification_id,
        "notification_channel": sender.notification_channel,
    }


notification_tasks_registry: dict[NotificationChannels, Callable]
notification_tasks_registry = {"email": send_email}
