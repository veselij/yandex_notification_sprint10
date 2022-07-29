import os

RABBITMQ = os.getenv("RABBITMQ", "rabbitmq")

WELCOME_QUEUE = os.getenv("WELCOME_QUEUE", "auth.send-welcome")
UGC_COMMENT_LIKE_QUEUE = os.getenv("UGC_COMMENT_LIKE_QUEUE", "ugc.comment-like")
ADMIN_QUEUE = os.getenv("ADMIN_QUEUE", "admin.send")

WELCOME_TEMPLATE_ID = os.getenv("WELCOME_TEMPLATE_ID", 1)
UGC_COMMENT_LIKE_TEMPLATE_ID = os.getenv("UGC_COMMENT_LIKE_TEMPLATE_ID", 2)

BROKER_URL = os.getenv("BROKER_URL", "redis://redis:6379/0")

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://mongo:27017")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "notifications")


