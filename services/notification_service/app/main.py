# app/main.py
import os, json, pika, threading
from fastapi import FastAPI
from .db                 import user_states
from .leaderboard_state  import load_top10_usernames, save_top10_usernames
from .top10              import process_event
from .mailer             import send_email
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
AMQP_URL    = os.getenv("AMQP_URL")
TOP10_QUEUE = "top10-notify"

# 1) Enable CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2) A simple health-check so GET / returns 200
@app.get("/")
def index():
    return {"message": "Connected"}


def run_consumer():
    conn    = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
    channel = conn.channel()
    channel.queue_declare(queue=TOP10_QUEUE, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=TOP10_QUEUE, on_message_callback=on_message, auto_ack=False)
    print("🔔 Notification service listening…")
    channel.start_consuming()

@app.on_event("startup")
def startup_event():
    threading.Thread(target=run_consumer, daemon=True).start()

def on_message(ch, method, props, body):
    evt = json.loads(body)

    # process_event now gives us both emails AND the new top-10
    emails, new_top10 = process_event(evt, user_states, load_top10_usernames)

    # send all the emails
    for to, subj, email_body in emails:
        send_email(to, subj, email_body)
        print(f"[Notification] Sent email to {to}")

    # persist the new top-10 usernames
    save_top10_usernames(new_top10)

    # ack the message
    ch.basic_ack(delivery_tag=method.delivery_tag)
