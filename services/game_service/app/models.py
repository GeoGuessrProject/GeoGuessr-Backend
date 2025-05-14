from datetime import datetime, timezone

def new_user_profile(username, email):
    return {
        "username": username,
        "email": email,
        "games_played": 0,
        "total_score": 0,
        "average_score": 0,
        "current_game": {
            "score": 0,
            "round": 0,
            "location_history": [],
            "start_time": None,
            "end_time": None
        },
        "history": [],
        "last_login": None,
        "created_at": datetime.now(timezone.utc)
    }
