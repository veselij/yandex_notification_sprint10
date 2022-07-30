from functools import lru_cache

from core.config import MONGODB_COLLECTION, MONGODB_DATABASE, MONGODB_URI
from pymongo import MongoClient
from pymongo.collection import Collection

mongo_client: MongoClient = MongoClient(MONGODB_URI)


@lru_cache
def get_mongo() -> Collection:
    return mongo_client[MONGODB_DATABASE][MONGODB_COLLECTION]
