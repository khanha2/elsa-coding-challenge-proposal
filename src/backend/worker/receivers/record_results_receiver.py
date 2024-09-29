from core.services.rabbitmq import connection
from core.domains.quiz.actions import write_participant


def start():
    channel = connection.create_channel()

    def callback(ch, method, properties, body):
        write_participant(body)

    channel.basic_consume(
        queue='record_results', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()
