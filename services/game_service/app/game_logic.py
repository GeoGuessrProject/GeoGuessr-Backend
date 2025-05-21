from app.db import user_states
from datetime import datetime, timezone


def get_user(username):
    return user_states.find_one({"username": username})

def start_game_for_user(username):
    return user_states.update_one(
        {"username": username},
        {"$set": {
            "current_game": {
                "score": 0,
                "round": 1,
                "location_history": [],
                "start_time": datetime.now(timezone.utc),
                "end_time": None
            }
        }}
    )

def update_guess(username, guess, correct_answer):
    correct = guess.strip().lower() == correct_answer.strip().lower()
    score_delta = 100 if correct else 0

    user_states.update_one(
        {"username": username},
        {
            "$inc": {
                "current_game.score": score_delta,
                "current_game.round": 1
            },
            "$push": {
                "current_game.location_history": {"guess": guess, "correct": correct}
            }
        }
    )
    return correct

def end_game_for_user(username):
    user = get_user(username)
    if not user or not user.get("current_game") or not user["current_game"].get("start_time"):
        return {"error": "No game in progress"}

    current_game = user["current_game"]
    current_game["end_time"] = datetime.now(timezone.utc)

    total_score = user.get("total_score", 0) + current_game["score"]
    games_played = user.get("games_played", 0) + 1
    average_score = total_score / games_played

    user_states.update_one(
        {"username": username},
        {
            "$push": {"history": current_game},
            "$set": {
                "current_game": {
                    "score": 0,
                    "round": 0,
                    "location_history": [],
                    "start_time": None,
                    "end_time": None
                },
                "games_played": games_played,
                "total_score": total_score,
                "average_score": average_score
            }
        }
    )
    return {
        "message": "Game ended",
        "username": user["username"],
        "email": user["email"],
        "new_score": current_game["score"],
        }



