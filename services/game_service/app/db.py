import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo:27017")
mongo_client = MongoClient(mongo_uri)
db = mongo_client["geodb"]
user_states = db["user_states"]

top10_scores   = db["top10_scores"]  # New collection for the top 10 scores
