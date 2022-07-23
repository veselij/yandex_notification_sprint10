from abc import ABC, abstractmethod
from typing import Literal

from distributions.services.userdata.base import UserData

NotificationChannels = Literal["email", "dummy"]


class BaseSender(ABC):

    notification_channel: NotificationChannels

    def __init__(self, user_data: UserData) -> None:
        self.user_data = user_data

    @abstractmethod
    def send(self, subject: str, content: str) -> None:
        ...
