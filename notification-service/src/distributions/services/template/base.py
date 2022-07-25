from abc import ABC, abstractmethod

from distributions.services.userdata.base import UserData


class BaseTemplate(ABC):
    def __init__(self, template_id: str) -> None:
        self._template_id = template_id

    @abstractmethod
    def get_content(self, content: str, userdata: UserData) -> str:
        ...

    @abstractmethod
    def get_subject(self) -> str:
        ...
