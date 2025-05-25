# leaderboard_state.py
from db import db

state = db["leaderboard_state"]

def load_top10_usernames():
    doc = state.find_one({"_id": "top10_usernames"})
    return doc["users"] if doc else []

def save_top10_usernames(usernames):
    state.replace_one(
        {"_id": "top10_usernames"},
        {"users": usernames},
        upsert=True
    )
