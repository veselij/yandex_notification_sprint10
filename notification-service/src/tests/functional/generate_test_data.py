from uuid import uuid4

from pymongo.mongo_client import MongoClient
from settings import MONGO_COLLECTION, MONGO_DB, MONGO_HOST, MONGO_PORT


def main():
    client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
    collection = client[MONGO_DB][MONGO_COLLECTION]
    for _ in range(10):
        user_id = str(uuid4())
        id = str(uuid4())
        name = "new_user"
        cont_id = str(uuid4())
        content = "link for registration"
        template_id = str(uuid4())
        schema = {
            "user_id": user_id,
            "notification_id": id,
            "notification_name": name,
            "content_id": cont_id,
            "content_value": content,
            "template_id": template_id,
        }

        collection.insert_one(schema)


if __name__ == "__main__":
    main()
