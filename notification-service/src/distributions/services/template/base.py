from abc import ABC, abstractmethod


class BaseTemplate(ABC):
    def __init__(self, template_id: str) -> None:
        self._template_id = template_id

    @abstractmethod
    def get_content(self, content: str, name: str) -> str:
        ...
