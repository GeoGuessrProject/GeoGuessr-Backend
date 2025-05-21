import os, json, datetime, pika
from bson import ObjectId
from db import scores                                   # ← import shared conn

AMQP_URL = os.getenv("AMQP_URL")

def current_top10():
    return list(
        scores.find().sort([("score", -1), ("created_at", 1)]).limit(10)
    )

def main():
    conn = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
    ch   = conn.channel()

    ch.queue_declare(queue="game.finished",      durable=True)
    ch.queue_declare(queue="leaderboard.dropped", durable=True)

    def callback(ch, method, properties, body):
        msg = json.loads(body)
        before = current_top10()

        scores.insert_one({
            "user_id":   ObjectId(msg["user_id"]),
            "username":  msg["username"],
            "score":     int(msg["score"]),
            "created_at": datetime.datetime.fromisoformat(msg["created_at"])
        })

        after = current_top10()

        lost_ids = {d["_id"] for d in before} - {d["_id"] for d in after}
        for lost in scores.find({"_id": {"$in": list(lost_ids)}}):
            ch.basic_publish(
                exchange="",
                routing_key="leaderboard.dropped",
                body=json.dumps({
                    "user_id": str(lost["user_id"]),
                    "username": lost["username"],
                    "score":    lost["score"]
                }),
                properties=pika.BasicProperties(delivery_mode=2)
            )
        ch.basic_ack(method.delivery_tag)

    ch.basic_qos(prefetch_count=10)
    ch.basic_consume("game.finished", callback)
    ch.start_consuming()

if __name__ == "__main__":
    main()
