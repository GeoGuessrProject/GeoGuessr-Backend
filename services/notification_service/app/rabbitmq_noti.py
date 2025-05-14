import json
import pika
import os
import threading
from app.top10 import update_top10

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
rabbitmq_user = os.getenv("RABBITMQ_USER", "guest")
rabbitmq_pass = os.getenv("RABBITMQ_PASS", "guest")
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)

def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        if data.get("event") == "game_ended":
            print(f"[TOP10] Received game_ended for {data['username']} with score {data['score']}")
            update_top10(data["username"], data["score"])
    except Exception as e:
        print(f"[TOP10] Error processing score event: {e}")

def start_score_event_listener():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue="score_events", durable=True)
    channel.basic_consume(queue="score_events", on_message_callback=callback, auto_ack=True)
    print("[TOP10] Listening to score_events...")
    channel.start_consuming()

def start_score_event_thread():
    thread = threading.Thread(target=start_score_event_listener, daemon=True)
    thread.start()


