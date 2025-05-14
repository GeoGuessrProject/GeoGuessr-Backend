import pika
import json
import os
import threading
from datetime import datetime, timezone
from dotenv import load_dotenv
from services.game_service.app.db import user_states
from services.game_service.app.models import new_user_profile

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")


def handle_user_registered(data):
    username = data["username"]
    print(f"[GAME SERVICE] User registered: {username}")
    
    if not user_states.find_one({"username": username}):
        user_states.insert_one(new_user_profile(username))
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
    print(f"[GAME SERVICE] Connected to RabbitMQ on host {RABBITMQ_HOST}")
    print("[GAME SERVICE] Listening to auth_events...")
    channel.start_consuming()


def start_consumer_thread():
    thread = threading.Thread(target=start_listening, daemon=True)
    thread.start()
