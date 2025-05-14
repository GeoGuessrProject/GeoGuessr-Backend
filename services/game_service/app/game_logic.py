"""All game‑state mutations live here so they’re easy to test."""
from datetime import datetime, timezone

from app.db import get_collection
from app.rabbitmq_game import notify_game_ended

user_states = get_collection("user_states")

# ── Gameplay constants ───────────────────────────────────────────────────────
MAX_ROUNDS     = 2
CORRECT_SCORE  = 100
EMPTY_GAME = {
    "score": 0,
    "round": 0,
    "location_history": [],
    "start_time": None,
    "end_time": None,
}


# ── Private helpers ──────────────────────────────────────────────────────────

def _utcnow():
    return datetime.utcnow().replace(tzinfo=timezone.utc)


def _calc_average(total: int, games: int) -> float:
    return total / games if games else 0.0


# ── Public API ───────────────────────────────────────────────────────────────

def get_user(username: str):
    return user_states.find_one({"username": username})


def start_game_for_user(username: str):
    """Initialise `current_game` and set `start_time`."""
    return user_states.update_one(
        {"username": username},
        {"$set": {
            "current_game": {
                **EMPTY_GAME,
                "round": 1,
                "start_time": _utcnow(),
            }
        }}
    )


def update_guess(username: str, guess: str) -> bool:
    """Apply a single guess and return True if it was correct."""
    correct      = guess.lower() == "paris"
    score_delta  = CORRECT_SCORE if correct else 0

    user_states.update_one(
        {"username": username},
        {
            "$inc": {
                "current_game.score":  score_delta,
                "current_game.round":  1,
            },
            "$push": {
                "current_game.location_history": {
                    "guess": guess,
                    "correct": correct,
                }
            },
        },
    )
    return correct


def end_game_for_user(username: str):
    """Finalize the game, update aggregates and broadcast `score_events`."""
    user = get_user(username)
    if not user or not user.get("current_game", {}).get("start_time"):
        return {"error": "No game in progress"}

    current_game         = user["current_game"]
    current_game["end_time"] = _utcnow()

    total_score   = user.get("total_score", 0) + current_game["score"]
    games_played  = user.get("games_played", 0) + 1
    average_score = _calc_average(total_score, games_played)

    # Notify other services *before* we reset the game field
    notify_game_ended(
        username=username,
        score_delta=current_game["score"],
        total_score=total_score,
    )

    update_doc = {
        "$push": {"history": current_game},
        "$set":  {
            "current_game": EMPTY_GAME,
            "games_played": games_played,
            "total_score":  total_score,
            "average_score": average_score,
        },
    }
    user_states.update_one({"username": username}, update_doc)
    return {"message": "Game ended"}