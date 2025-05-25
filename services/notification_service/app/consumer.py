import os, json, pika
from db import user_states           # same shared db.py
from services.notification_service.app.mildertidig.mail import send_email  
from datetime import datetime
   # your existing SMTP helper

AMQP_URL = os.getenv("AMQP_URL")
QUEUE    = "top10-notify"

def on_message(ch, method, props, body):
    evt      = json.loads(body)
    username = evt["username"]

    # 1) Fetch the top 11 by score desc, then by last_end_time asc
    top11 = list(
      user_states
      .find({}, {"username":1,"email":1,"total_score":1,"last_end_time":1})
      .sort([("total_score", -1), ("last_end_time", 1)])
      .limit(11)
    )

    # 2) If the user who just played is now in top 10, then the #11 slot got bumped
    in_top10 = any(u["username"] == username for u in top11[:10])
    if in_top10 and len(top11) == 11:
        bumped = top11[10]
        send_email(
          to      = bumped["email"],
          subject = "You fell out of the Top 10!",
          body    = (
            f"Hi {bumped['username']},\n\n"
            f"Your score of {bumped['total_score']} just got overtaken—you’re now #11. Time for a rematch!\n\n— The Team"
          )
        )

    print(f"[Notification] Sent Top-10 drop email to {bumped['username']}" if in_top10 else "[Notification] No Top-10 drop email sent")

    # 3) ACK the message so RabbitMQ can delete it
    ch.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == "__main__":
    conn    = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
    channel = conn.channel()
    channel.queue_declare(queue=QUEUE, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE, on_message_callback=on_message, auto_ack=False)
    print("🔔 Waiting for top-10 notifications…")
    channel.start_consuming()
