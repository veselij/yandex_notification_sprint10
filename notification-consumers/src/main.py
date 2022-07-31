import logging

import pika
from core.config import ADMIN_QUEUE, RABBITMQ, UGC_COMMENT_LIKE_QUEUE, WELCOME_QUEUE
from workers.admin import callback as admin_callback
from workers.likes import callback as likes_callback
from workers.welcome import callback as welcome_callback


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ, virtual_host="vhost")
    )
    channel = connection.channel()

    channel.queue_declare(UGC_COMMENT_LIKE_QUEUE, durable=True)
    channel.basic_consume(UGC_COMMENT_LIKE_QUEUE, likes_callback)

    channel.queue_declare(WELCOME_QUEUE, durable=True)
    channel.basic_consume(WELCOME_QUEUE, welcome_callback)

    channel.queue_declare(ADMIN_QUEUE, durable=True)
    channel.basic_consume(ADMIN_QUEUE, admin_callback)

    try:
        logging.info("Start consuming")
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()

    connection.close()


if __name__ == "__main__":
    main()
