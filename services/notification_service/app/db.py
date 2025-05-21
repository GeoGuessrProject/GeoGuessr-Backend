import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))       # 1 env var for every svc
db      = client["geoguessr"]                        # ← same DB everywhere

scores  = db["scores"]       # new collection you asked for


scores.create_index(
    [("score", -1), ("created_at", 1)],
    name="score_rank_idx"
)