from typing import Optional

import pymongo.mongo_client as mongo
from celery import Task
from celery.utils.log import get_task_logger
from distributions.services.exceptions import RepeatTaskExceptionError
from distributions.services.notification.base import DBConnection
from distributions.services.notification.mongo import MongoDBConnection
from django.conf import settings
from pymongo.errors import (
    ConnectionFailure,
    CursorNotFound,
    ExecutionTimeout,
    NetworkTimeout,
    ServerSelectionTimeoutError,
    WriteError,
)
from requests.exceptions import ReadTimeout, Timeout

logger = get_task_logger(__name__)


class BaseTaskWithRetry(Task):
    max_retries = 3
    retry_backoff = True
    retry_backoff_max = 700
    retry_jitter = True
    task_ignore_result = True
    task_acks_late = True


class RequestsTaskRetry(BaseTaskWithRetry):
    autoretry_for = (Timeout, ReadTimeout)


class SendTaskRetry(BaseTaskWithRetry):
    autoretry_for = (RepeatTaskExceptionError,)
    rate_limit = "1/s"


class MongoTaskWithRetry(BaseTaskWithRetry):
    autoretry_for = (
        ConnectionFailure,
        CursorNotFound,
        NetworkTimeout,
        ServerSelectionTimeoutError,
        WriteError,
        ExecutionTimeout,
    )
    _db: Optional[DBConnection] = None

    @property
    def db(self) -> DBConnection:
        if self._db is None:
            client: mongo.MongoClient = mongo.MongoClient(
                settings.MONGO_HOST, settings.MONGO_PORT
            )
            self._db = MongoDBConnection(
                client[settings.MONGO_DB][settings.MONGO_COLLECTION]
            )
            logger.info(
                "Connected to MONGO HOST %s PORT %d COLLECTION %s",
                settings.MONGO_HOST,
                settings.MONGO_PORT,
                settings.MONGO_COLLECTION,
            )
        return self._db
