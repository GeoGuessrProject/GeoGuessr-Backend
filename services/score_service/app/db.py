import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
mongo_client = MongoClient(mongo_uri, server_api=ServerApi('1'))

db = mongo_client["geodb"]

# Only access collections relevant for this service:
user_states = db["user_states"]
top10_scores = db["top10_scores"]