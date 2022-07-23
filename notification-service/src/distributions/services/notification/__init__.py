from typing import Type

from config.settings import DEBUG
from distributions.services.notification.base import (
    BaseNotificaionClient,
    DBNotificaionClient,
)
from distributions.services.notification.dummy import DummyNotificationClient

NotificationClient: Type[BaseNotificaionClient]
if DEBUG:
    NotificationClient = DummyNotificationClient
else:
    NotificationClient = DBNotificaionClient
