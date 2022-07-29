import pika
import pymongo
import pytest
import redis


@pytest.fixture(scope='session')
def mongodb_client():
    connection = pymongo.MongoClient("mongodb://mongo:27017")
    yield connection
    connection.close()


@pytest.fixture(scope='session')
def rabbitmq_client():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    yield connection
    connection.close()

@pytest.fixture(scope='session')
def redis_client():
    connection = redis.Redis(host='redis', port=6379, db=0)
    yield connection
    connection.close()
