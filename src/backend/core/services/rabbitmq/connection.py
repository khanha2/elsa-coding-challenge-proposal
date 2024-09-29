import os
import urllib.parse

import pika
import pika.connection


def create_channel():
    connection = pika.BlockingConnection(
        pika.connection.URLParameters(os.getenv('RABBITMQ_URL'))
    )
    return connection.channel()
