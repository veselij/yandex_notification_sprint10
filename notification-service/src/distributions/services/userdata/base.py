from abc import ABC, abstractmethod

from pydantic import BaseModel


class UserData(BaseModel):
    class Config:
        allow_mutation = False

    user_id: str
    timezone: int
    name: str
    email: str
    mobile: str
    notification_policy: bool


class BaseUserDataClient(ABC):
    @abstractmethod
    def get_user_data(self, user_id: str) -> UserData:
        ...
