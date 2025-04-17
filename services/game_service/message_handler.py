import pika
import json
import os
import threading
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime, timezone

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")

mongo_client = MongoClient(os.getenv("MONGO_HOST", "mongo"), 27017)
db = mongo_client["geodb"]
user_states = db["user_states"]

def handle_user_registered(data):
    print(f"[GAME SERVICE] User registered: {data['username']}")
    
    existing = user_states.find_one({"username": data["username"]})
    if not existing:
        user_states.insert_one({
            "username": data["username"],
            "games_played": 0,
            "current_game": {
                "score": 0,
                "round": 0,
                "location_history": [],  # could hold coordinates/guesses
                "start_time": None,
                "end_time": None
            },
            "history": [],  # store past game sessions if you want to track stats
            "last_login": None,
            "created_at": datetime.now(timezone.utc)
        })
        print(f"[GAME SERVICE] Initialized extended game profile for {data['username']}")


def handle_user_logged_in(data):
    print(f"[GAME SERVICE] User logged in: {data['username']}")
    
    user_states.update_one(
        {"username": data["username"]},
        {"$set": {"last_login": datetime.now(timezone.utc)}},
        upsert=True
    )


def callback(ch, method, properties, body):
    try:
        message = json.loads(body)
        event_type = message.get("event")

        if event_type == "user_registered":
            handle_user_registered(message)
        elif event_type == "user_logged_in":
            handle_user_logged_in(message)
        else:
            print(f"[GAME SERVICE] Unknown event: {event_type}")
    except Exception as e:
        print(f"[GAME SERVICE] Error processing message: {e}")

def start_listening():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue="auth_events", durable=True)

    channel.basic_consume(queue="auth_events", on_message_callback=callback, auto_ack=True)

    print("[GAME SERVICE] Listening to auth_events...")
    channel.start_consuming()

# Run this in a thread so it doesn't block the FastAPI app
def start_consumer_thread():
    thread = threading.Thread(target=start_listening)
    thread.daemon = True
    thread.start()
