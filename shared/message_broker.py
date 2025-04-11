import pika, os
from dotenv import load_dotenv
load_dotenv()

def publish_message(queue: str, message: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv("RABBITMQ_HOST")))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange='', routing_key=queue, body=message)
    connection.close()
