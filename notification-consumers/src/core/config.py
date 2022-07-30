import os

RABBITMQ = os.getenv("RABBITMQ", "rabbitmq")

WELCOME_QUEUE = os.getenv("WELCOME_QUEUE", "auth.send-welcome")
UGC_COMMENT_LIKE_QUEUE = os.getenv("UGC_COMMENT_LIKE_QUEUE", "ugc.comment-like")
ADMIN_QUEUE = os.getenv("ADMIN_QUEUE", "admin.send")

BROKER_URL = os.getenv("BROKER_URL", "redis://redis:6379/0")

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://mongo:27017")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "notifications")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "notifications")
