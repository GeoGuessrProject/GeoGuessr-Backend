import pika
import json
import os
import threading
from datetime import datetime, timezone
from dotenv import load_dotenv
from app.db import user_states
from app.models import new_user_profile
from pika.exceptions import AMQPConnectionError

connection = None
channel = None

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")

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


def handle_user_registered(data):
    username = data["username"]
    email = data["email"]
    print(f"[GAME SERVICE] User registered: {username}")
    
    if not user_states.find_one({"username": username}):
        user_states.insert_one(new_user_profile(username, email))
    print(f"[GAME SERVICE] Initialized profile for {username}")


def handle_user_logged_in(data):
    username = data["username"]
    print(f"[GAME SERVICE] User logged in: {username}")
    
    user_states.update_one(
        {"username": username},
        {"$set": {"last_login": datetime.now(timezone.utc)}},
        upsert=True
    )


def callback(ch, method, properties, body):
    try:
        message = json.loads(body)
        event = message.get("event")

        match event:
            case "user_registered":
                handle_user_registered(message)
            case "user_logged_in":
                handle_user_logged_in(message)
            case _:
                print(f"[GAME SERVICE] Unknown event type: {event}")
    except Exception as e:
        print(f"[GAME SERVICE] Error processing message: {e}")


def start_listening():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, heartbeat=30))
    channel = connection.channel()
    channel.queue_declare(queue="auth_events", durable=True)
    channel.basic_consume(queue="auth_events", on_message_callback=callback, auto_ack=True)

    print("[GAME SERVICE] Listening to auth_events...")
    channel.start_consuming()


def start_consumer_thread():
    thread = threading.Thread(target=start_listening, daemon=True)
    thread.start()

def notify_game_ended(username: str, score: int):
    send_message("score_events", {
        "event": "game_ended",
        "username": username,
        "score": score
    })
    
def notify_game_ended(username: str, score_delta: int, total_score: int):
    """Emit a `score_events` message so other services stay in sync."""
    send_message(
        "score_events",
        {
            "event": "game_ended",
            "username": username,
            "score_delta": score_delta,
            "total_score": total_score,
        },
    )