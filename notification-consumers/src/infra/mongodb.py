from functools import lru_cache
from pymongo import MongoClient
from typing import Optional

from core.config import MONGODB_URI, MONGODB_DATABASE

mongo_client: Optional[MongoClient] = MongoClient(MONGODB_URI)


@lru_cache
def get_mongo() -> MongoClient:
    if mongo_client:
        return mongo_client[MONGODB_DATABASE]
