from core.services.rabbitmq import connection


def start():
    channel = connection.create_channel()

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    channel.basic_consume(
        queue='record_results', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()
