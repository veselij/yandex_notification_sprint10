import os

# MONGO settings
MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017))
MONGO_DB = os.environ.get("MONGO_DB", "test_db")
MONGO_COLLECTION = os.environ.get("MONGO_COLLECTION", "test_collection")
