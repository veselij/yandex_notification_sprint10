from typing import Union

from pydantic import BaseModel


class Message(BaseModel):
    notification_name: str
    user_id: str
    template_id: str
    content_id: str
    content_value: Union[str, int]


class Notification(BaseModel):
    notification_id: str
    notification_name: str
    user_id: str
    template_id: str
    content_id: str
    content_value: Union[str, int]
