# models.py
from pymongo import MongoClient, ASCENDING, DESCENDING
from app.config import Config

cfg = Config()
client = MongoClient(cfg.mongo_uri)
db     = client["geo"]         # use the same DB-name as in your FastAPI/db.py
scores = db["scores"]
scores.create_index([("score", DESCENDING), ("ts", ASCENDING)])