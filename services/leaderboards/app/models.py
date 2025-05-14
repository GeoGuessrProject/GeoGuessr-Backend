# models.py
from pymongo import MongoClient, ASCENDING, DESCENDING
from config import Config

client = MongoClient(Config.MONGO_URI)
db     = client["leaderboard"]
scores = db["scores"]

# For fast top-10 queries:
scores.create_index([("score", DESCENDING), ("ts", ASCENDING)])