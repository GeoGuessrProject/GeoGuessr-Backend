from __future__ import annotations

from typing import Any, List

from fastapi import Depends, FastAPI
from pydantic import BaseModel

from .db import get_scores
from pymongo.collection import Collection

app = FastAPI(title="GeoGuessr Leaderboards")


class ScoreOut(BaseModel):
    user_id: str
    username: str
    score: int


@app.get("/top10", response_model=List[ScoreOut])
async def read_top10(scores: Collection = Depends(get_scores)) -> List[dict[str, Any]]: # noqa: D401
    """Return the live Top 10, sorted by score descending."""
    pipeline = [
        {"$setWindowFields": {"sortBy": {"score": -1}, "output": {"rank": {"$rank": {}}}}},
        {"$match": {"rank": {"$lte": 10}}},
        {"$project": {"_id": 0, "user_id": 1, "username": 1, "score": 1}},
    ]
    cursor = scores.aggregate(pipeline)
    return [doc async for doc in cursor]