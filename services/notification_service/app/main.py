# main.py

import os, json, pika
from top10 import process_event
from db import user_states
from leaderboard_state import load_top10_usernames, save_top10_usernames

AMQP_URL    = os.getenv("AMQP_URL")
TOP10_QUEUE = "top10-notify"

def on_message(ch, method, props, body):
    evt = json.loads(body)
    # delegate all the “who to email?” logic to top10.process_event
    emails_to_send = process_event(evt, user_states, load_top10_usernames)
    # send them
    from mailer import send_email
    for to, subj, body in emails_to_send:
        send_email(to, subj, body)
    # persist the new top10
    save_top10_usernames([u for u in process_event.latest_top10])
    # ACK
    ch.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == "__main__":
    conn    = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
    channel = conn.channel()
    channel.queue_declare(queue=TOP10_QUEUE, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
      queue=TOP10_QUEUE,
      on_message_callback=on_message,
      auto_ack=False
    )
    print("🔔 Notification service listening…")
    channel.start_consuming()
