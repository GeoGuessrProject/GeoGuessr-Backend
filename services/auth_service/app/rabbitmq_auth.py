import pika
import json
import os
from pika.exceptions import AMQPConnectionError

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")

# Keep persistent connection and channel as globals
connection = None
channel = None

def init_rabbitmq():
    global connection, channel
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, heartbeat=30)
        )
        channel = connection.channel()
        print("[AUTH SERVICE] Connected to RabbitMQ.")
    except AMQPConnectionError as e:
        print(f"[AUTH SERVICE] Failed to connect to RabbitMQ: {e}")
        connection = None
        channel = None

def send_message(queue_name: str, message: dict):
    global channel

    if channel is None or connection is None or connection.is_closed:
        init_rabbitmq()

    if channel is None:
        print("[AUTH SERVICE] Cannot send message — no RabbitMQ channel.")
        return

    try:
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        print(f"[AUTH SERVICE] Sent message to {queue_name}: {message}")
    except Exception as e:
        print(f"[AUTH SERVICE] Failed to send message: {e}")
