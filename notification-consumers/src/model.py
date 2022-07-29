import datetime
from pydantic import BaseModel
from typing import Optional


class Message(BaseModel):
    notification_name: str
    user_id: str
    template_id: Optional[str]
    content_id: Optional[str]
    content_value: Optional[str]


class Notification(BaseModel):
    notification_id: str
    notification_name: str
    user_id: str
    template_id: Optional[str]
    content_id: Optional[str]
    content_value: Optional[str]
    last_updated: datetime.datetime
