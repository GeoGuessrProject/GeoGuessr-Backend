# mail_service.py
import os, json, smtplib
from email.message import EmailMessage
from celery import Celery

celery_app = Celery(
    "mail_service",
    broker=os.getenv("AMQP_URL"),       # e.g. amqp://guest:guest@rabbitmq//
)

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")


@celery_app.task(queue="leaderboard.dropped")
def notify_drop(event_json):
    evt = json.loads(event_json)

    # Pull e-mail from Mongo (or MySQL if that is canonical)
    from pymongo import MongoClient
    user = (MongoClient(os.getenv("MONGODB_URI"))
           .geoguessr.users
           .find_one({"_id": evt["user_id"]}))

    if not user or "email" not in user:
        return

    msg = EmailMessage()
    msg["Subject"] = "You just fell off the top-10!"
    msg["From"]    = "noreply@mockgeoguessr.xyz"
    msg["To"]      = user["email"]
    msg.set_content(
        f"Hi {evt['username']},\n\n"
        f"Your score of {evt['score']} was pushed out of the top-10.\n"
        f"Time to reclaim your spot!\n\n"
        "Happy guessing 👀🌍"
    )

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        s.starttls()
        s.login(SMTP_USER, SMTP_PASS)
        s.send_message(msg)
