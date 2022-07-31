from datetime import datetime
from typing import Any

from distributions.services.notification.base import DBConnection, NotificationResult
from pymongo.collection import Collection


class MongoDBConnection(DBConnection):
    def __init__(self, db: Collection) -> None:
        self.db = db

    def update_one(self, notification_result: NotificationResult) -> Any:
        self.db.update_one(
            {"notification_id": notification_result["notification_id"]},
            {
                "$set": {
                    notification_result[
                        "notification_channel"
                    ]: datetime.now().timestamp()
                }
            },
        )

    def get_rows(self, event_name: str) -> Any:
        return self.db.find({"notification_name": event_name}, max_time_ms=10000)

    def get_content(self, notification_id: str) -> Any:
        notification = self.db.find_one(
            {"notification_id": notification_id}, max_time_ms=10000
        )
        return notification

    def insert_or_update(
        self,
        user_id: str,
        notification_id: str,
        notification_name: str,
        content_id: str,
        content_value: str,
        template_id: str,
    ) -> Any:
        self.db.update_one(
            {"notification_name": notification_name, "user_id": user_id},
            {
                "$set": {
                    "notification_id": notification_id,
                    "notification_name": notification_name,
                    "user_id": user_id,
                    "content_id": content_id,
                    "content_value": content_value,
                    "template_id": template_id,
                }
            },
            upsert=True,
        )
