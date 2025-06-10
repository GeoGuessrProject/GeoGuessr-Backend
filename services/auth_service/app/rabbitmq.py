import pika
import json
import os
import time
from pika.exceptions import AMQPConnectionError

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")

connection = None
channel = None

def init_rabbitmq(max_retries=5, delay=3):
    global connection, channel
    for attempt in range(1, max_retries + 1):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST, heartbeat=600)
            )
            channel = connection.channel()
            print("[AUTH SERVICE] Connected to RabbitMQ.")
            return
        except AMQPConnectionError as e:
            print(f"[AUTH SERVICE] RabbitMQ connection failed (attempt {attempt}): {e}")
            time.sleep(delay)
    connection = None
    channel = None
    print("[AUTH SERVICE] Could not connect to RabbitMQ after retries.")

def send_message(queue_name: str, message: dict):
    global channel, connection

    if channel is None or connection is None or connection.is_closed or channel.is_closed:
        init_rabbitmq()

    if channel is None or channel.is_closed:
        print("[AUTH SERVICE] Cannot send message — no valid RabbitMQ channel.")
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
