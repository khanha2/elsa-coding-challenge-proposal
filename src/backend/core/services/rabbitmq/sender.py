import json

from .connection import create_channel

channel = create_channel()


def send_message(queue_name: str, message: dict | list):
    print(message)
    channel.basic_publish(
        exchange='', routing_key=queue_name, body=json.dumps(message)
    )
