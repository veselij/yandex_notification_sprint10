from typing import Generator
from uuid import uuid4

from distributions.services.notification.base import (
    BaseNotificaionClient,
    DBConnection,
    Notification,
    NotificationResult,
)


class DummyNotificationClient(BaseNotificaionClient):
    def __init__(self, db: DBConnection) -> None:
        self._db = db

    def get_notifications(self, event_name: str) -> Generator[Notification, None, None]:
        for _ in range(1):
            yield Notification(
                id=str(uuid4()),
                user_id=str(uuid4()),
                template_id=str(uuid4()),
            )

    def update_notification(self, notification_result: NotificationResult) -> None:
        print(
            f"notification status for {notification_result['notification_id']} update in {notification_result['notification_channel']}"
        )

    def get_notification_content(self, notification_id: str) -> dict:
        return {"content_value": "test_content"}
