"""Celery task that detects when users drop out of the Top 10 and mails them."""
import redis
from celery import Celery

from config import Config
from db import user_states
from mailer import send_fallen_email


celery = Celery("leaderboards", broker=Config.broker_url())
celery.conf.update(task_serializer="json", result_serializer="json")

# ── Redis keys & constants ───────────────────────────────────────────────────
r        = redis.Redis()
TOP_N    = 10
SNAP_KEY = "leaderboard:top10"  # list of current Top N usernames

# Add a beat entry directly in code so no extra config file is required.
celery.conf.beat_schedule = {
    "scan-every-30s": {
        "task": "leaderboards.tasks.scan_leaderboard",
        "schedule": 30.0,
    }
}


@celery.task
def scan_leaderboard():
    """Compare current Top 10 to last tick; e‑mail anyone who fell out."""
    # 1. Current Top N
    pipeline = [
        {"$sort": {"total_score": -1, "created_at": 1}},
        {"$limit": TOP_N},
        {"$project": {"_id": 0, "username": 1}},
    ]
    now_top = [doc["username"] for doc in user_states.aggregate(pipeline)]

    # 2. Previous snapshot
    last_top = [u.decode() for u in r.lrange(SNAP_KEY, 0, -1)]

    # 3. Who fell out?
    fallen = set(last_top) - set(now_top)
    if fallen:
        rank_pipeline = [
            {"$setWindowFields": {
                "sortBy": {"total_score": -1, "created_at": 1},
                "output": {"rank": {"$rank": {}}},
            }},
            {"$match": {"username": {"$in": list(fallen)}}},
            {"$project": {"_id": 0, "username": 1, "rank": 1, "email": 1}},
        ]
        for doc in user_states.aggregate(rank_pipeline):
            email = doc.get("email")
            if not email:
                continue  # no e‑mail on file
            sent_flag = f"sent:{doc['username']}:{doc['rank']}"
            if not r.set(sent_flag, 1, nx=True, ex=86_400):
                continue  # already mailed within the last 24 h
            send_fallen_email(doc["username"], email, doc["rank"])

    # 4. Persist snapshot for next tick
    with r.pipeline() as pipe:
        pipe.delete(SNAP_KEY)
        if now_top:
            pipe.rpush(SNAP_KEY, *now_top)
        pipe.execute()