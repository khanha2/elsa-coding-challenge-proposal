import json

from core.services.rabbitmq import connection, sender
from core.domains.quiz.actions import write_participant


def start():
    channel = connection.create_channel()

    def callback(ch, method, properties, body):
        write_participant(body)
        sender.send_message('message_broadcasting', json.loads(body))

    channel.basic_consume(
        queue='record_results', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()
