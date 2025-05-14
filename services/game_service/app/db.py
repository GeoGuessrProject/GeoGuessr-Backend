import os
from pymongo import MongoClient
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo:27017")
mongo_client = MongoClient(mongo_uri)
db = mongo_client["geodb"]
user_states = db["user_states"] 



@lru_cache(maxsize=1)
def get_client() -> MongoClient:
    """Return a singleton, tz‑aware Mongo client."""
    return MongoClient(mongo_uri, tz_aware=True)


def get_collection(name: str, db_name: str = "geodb"):
    """Shortcut for *any* collection so tests can swap DB names."""
    return get_client()[db_name][name]