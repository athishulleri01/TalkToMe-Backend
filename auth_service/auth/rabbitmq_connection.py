import pika
from django.conf import settings

def get_rabbitmq_connection():
    credentials = pika.PlainCredentials(
        username=settings.RABBITMQ_USERNAME,
        password=settings.RABBITMQ_PASSWORD
    )

    parameters = pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        virtual_host=settings.RABBITMQ_VIRTUAL_HOST,
        credentials=credentials
    )

    connection = pika.BlockingConnection(parameters)
    return connection