"""Celery tasks that maintain the live leaderboard."""
from __future__ import annotations
import asyncio
import datetime as _dt
import json
import logging
from typing import Any, Final, List

import celery
import redis
from bson import Int64

from app import cfg
from .db import _scores
from .mailer import send_fallen_email

LOGGER = logging.getLogger(__name__)

# ------------------ Celery setup -------------------------
app = celery.Celery("leaderboards")
app.conf.broker_url = cfg.broker_url
app.conf.result_backend = f"redis://{cfg.redis_host}/0"

REDIS: Final = redis.Redis(host=cfg.redis_host, decode_responses=True)
SNAPSHOT_KEY: Final = "leaderboard:snapshot"  # JSON‑encoded list of top‑10 user_ids
MAIL_COOLDOWN_HOURS: Final = 24


# ------------------ Helpers ------------------------------

async def _current_top10_ids() -> List[str]:
    """Return list of user_ids currently in Top 10 (highest score wins)."""
    pipeline: List[Any] = [
        {"$setWindowFields": {"sortBy": {"score": -1}, "output": {"rank": {"$rank": {}}}}},
        {"$match": {"rank": {"$lte": Int64(10)}}},
        {"$project": {"_id": 0, "user_id": 1}},
    ]
    cursor = _scores.aggregate(pipeline)
    return [doc["user_id"] async for doc in cursor]  # type: ignore[misc]


def _load_previous_snapshot() -> list[str]:
    raw = REDIS.get(SNAPSHOT_KEY)
    return json.loads(raw) if raw else []


def _store_snapshot(user_ids: list[str]) -> None:
    REDIS.set(SNAPSHOT_KEY, json.dumps(user_ids))


# ------------------ Main periodic task -------------------

@app.on_after_configure.connect()
def _setup_periodic_tasks(sender: celery.Celery, **_: Any) -> None:  # noqa: D401 – signal name fixed
    sender.add_periodic_task(30.0, scan_leaderboard.s(), name="scan every 30 s")


@app.task(bind=True, name="scan_leaderboard")
async def scan_leaderboard(_: celery.Task) -> None:  # type: ignore[override]
    """Compare current top‑10 with last snapshot and notify displaced players."""
    try:
        current = await asyncio.run(_current_top10_ids())
        previous = _load_previous_snapshot()
        if not previous:
            _store_snapshot(current)
            return

        displaced = set(previous) - set(current)
        if not displaced:
            _store_snapshot(current)
            return

        LOGGER.info("Displaced players: %s", displaced)

        # Fetch e‑mails for displaced players in *one* DB call
        cursor = _scores.find({"user_id": {"$in": list(displaced)}})
        now = _dt.datetime.utcnow()
        for doc in await cursor.to_list(length=None):
            # cooldown check (so we don't spam)
            last_mail: _dt.datetime | None = doc.get("last_mail")  # type: ignore[assignment]
            if last_mail and (now - last_mail).total_seconds() < MAIL_COOLDOWN_HOURS * 3600:
                continue

            send_fallen_email(doc["email"], doc["username"], 10)  # old_rank was ≤10
            await _scores.update_one({"_id": doc["_id"]}, {"$set": {"last_mail": now}})

        _store_snapshot(current)
    except Exception as exc:  # pylint: disable=broad-except
        LOGGER.exception("scan_leaderboard failed: %s", exc)