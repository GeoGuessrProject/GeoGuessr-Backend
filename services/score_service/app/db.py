import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

mongo_client = MongoClient(os.getenv("MONGO_HOST", "mongo"), 27017)
db = mongo_client["geodb"]
user_states = db["user_states"]
