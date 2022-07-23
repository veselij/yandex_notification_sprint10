from abc import ABC, abstractmethod
from typing import Any, Generator, Literal, Protocol

from pydantic import BaseModel

NotificationResult = dict[Literal["notification_id", "notification_channel"], str]


class DBConnection(Protocol):
    def update_one(self, notification_result: NotificationResult) -> Any:
        ...

    def get_rows(self, event_name: str) -> Any:
        ...

    def get_content(self, notification_id: str) -> Any:
        ...


class Notification(BaseModel):
    class Config:
        allow_mutation = False

    id: str
    user_id: str
    template_id: str


class BaseNotificaionClient(ABC):
    def __init__(self, db: DBConnection) -> None:
        self.db = db

    @abstractmethod
    def get_notifications(self, event_name: str) -> Generator[Notification, None, None]:
        ...

    @abstractmethod
    def update_notification(self, notification_result: NotificationResult) -> None:
        ...

    @abstractmethod
    def get_notification_content(self, notification_id: str) -> dict:
        ...


class DBNotificaionClient(BaseNotificaionClient):
    def get_notifications(self, event_name: str) -> Generator[Notification, None, None]:
        for row in self.db.get_rows(event_name):
            print("123", row)
            yield Notification(
                id=row["notification_id"],
                user_id=row["user_id"],
                template_id=row["template_id"],
            )

    def update_notification(self, notification_result: NotificationResult) -> None:
        self.db.update_one(notification_result)

    def get_notification_content(self, notification_id: str) -> dict:
        return self.db.get_content(notification_id)
