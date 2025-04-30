# app/top10.py

import os
import json
from datetime import datetime, timezone

import pika
from app.db import top10_scores

from flask import Flask

app = Flask(__name__)

@app.route('/top10')
def get_top10():
    # call your top10 logic
    return {"top10": ["player1", "player2", "player3"]}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)

# RabbitMQ helper
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")

def publish_event(queue: str, message: dict):
    conn = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    ch = conn.channel()
    ch.queue_declare(queue=queue, durable=True)
    ch.basic_publish(
        exchange='',
        routing_key=queue,
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    conn.close()

def update_top10(username: str, score: int):
    """
    Inserts (username,score) into top10_scores if it qualifies,
    shifts lower entries down, removes the 11th, and notifies
    every user whose entry was pushed down.
    """
    now = datetime.now(timezone.utc)
    new_entry = {"username": username, "score": score, "timestamp": now}

    # 1) Fetch current Top 10 ordered by score desc, time asc
    current = list(
        top10_scores
          .find({}, {"_id":1, "username":1, "score":1, "timestamp":1})
          .sort([("score", -1), ("timestamp", 1)])
    )

    # 2) Check qualification
    if len(current) < 10:
        qualifies = True
    else:
        worst = current[-1]
        qualifies = (
            score > worst["score"]
            or (score == worst["score"] and now < worst["timestamp"])
        )
    if not qualifies:
        return

    # 3) Determine insertion index
    insert_idx = len(current)
    for idx, doc in enumerate(current):
        if (score > doc["score"]) or (
            score == doc["score"] and now < doc["timestamp"]
        ):
            insert_idx = idx
            break

    # 4) Insert new entry
    top10_scores.insert_one(new_entry)

    # 5) If more than 10 entries, delete the 11th
    all_after = list(
        top10_scores
          .find({}, {"_id":1, "username":1})
          .sort([("score", -1), ("timestamp", 1)])
    )
    if len(all_after) > 10:
        to_remove = all_after[10]
        top10_scores.delete_one({"_id": to_remove["_id"]})

    # 6) Notify anyone pushed down (from insert_idx onward in the old list)
    displaced = current[insert_idx:]
    for doc in displaced:
        publish_event("notification_events", {
            "event":    "leaderboard_displaced",
            "username": doc["username"],
            "by":       username,
            "new_score": score,
            "time":      now.isoformat()
        })
