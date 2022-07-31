from abc import ABC, abstractmethod

from distributions.models import NotificationTemplates
from distributions.services.sender.base import NotificationChannels
from distributions.services.userdata.base import UserData


class BaseTemplate(ABC):
    def __init__(self, template_id: str, channel: NotificationChannels) -> None:
        self._template_id = template_id
        self._channel = channel
        self.template = NotificationTemplates.objects.get(
            name=template_id, channel=channel
        )

    @abstractmethod
    def get_content(self, content: str, userdata: UserData) -> str:
        ...

    @abstractmethod
    def get_subject(self) -> str:
        ...
