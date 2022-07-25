import pymongo.mongo_client as mongo
import pytest
from tests.functional.settings import MONGO_COLLECTION, MONGO_DB, MONGO_HOST, MONGO_PORT


@pytest.fixture(scope="session")
def celery_config():
    return {"broker_url": "redis://localhost:6379/0"}


@pytest.fixture(scope="session")
def mongo_collection():
    return mongo.MongoClient(MONGO_HOST, MONGO_PORT)[MONGO_DB][MONGO_COLLECTION]
