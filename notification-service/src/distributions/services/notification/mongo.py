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
        return self.db.find({"notification_name": event_name})

    def get_content(self, notification_id: str) -> Any:
        return self.db.find_one({"notification_id": notification_id})
