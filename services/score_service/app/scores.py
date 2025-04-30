from fastapi import HTTPException
from app.db import user_states


def get_top_scores(limit):
    """
    Retrieve each user's single highest score (breaking ties by oldest start_time),
    then return the top scores across users.

    - **limit**: Maximum number of top scores to return (default: 10)
    """
    pipeline = [
        # Flatten each game record
        {"$unwind": "$history"},
        # Keep relevant fields
        {"$project": {
            "_id": 0,
            "username": 1,
            "score": "$history.score",
            "start_time": "$history.start_time",
            "end_time": "$history.end_time"
        }},
        # Sort by username (asc), score (desc), then start_time (asc) to break ties by oldest
        {"$sort": {"username": 1, "score": -1, "start_time": 1}},
        # Finally, sort globally by score desc, then by start_time asc for tie-breaks
        {"$sort": {"score": -1, "start_time": 1}},
        {"$limit": limit}
    ]
    try:
        results = list(user_states.aggregate(pipeline))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"top_scores": results}
