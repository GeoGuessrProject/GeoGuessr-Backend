from __future__ import annotations

import motor.motor_asyncio
from fastapi import Depends
from pymongo.collection import Collection

from app import cfg


_client = motor.motor_asyncio.AsyncIOMotorClient(cfg.mongo_uri)
_db = _client["geo"]  # database name
_scores: Collection = _db["scores"]


async def get_scores() -> Collection:
    """FastAPI dependency that yields the *scores* collection."""
    return _scores

# Expose the raw objects for non‑FastAPI modules (Celery tasks, etc.)
__all__ = ["_db", "_scores", "get_scores"]