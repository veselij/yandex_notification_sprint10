from time import sleep

from distributions.tasks import schedule_notifications
from tests.functional.testdata.data import notifications


def test_schedule_notifications(celery_worker, mongo_collection):
    mongo_collection.drop()
    mongo_collection.insert_many(notifications)
    schedule_notifications.delay("new_user", 1)
    sleep(2)
    for notification in mongo_collection.find():
        assert "dummy" in notification
