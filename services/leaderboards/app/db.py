"""Read‑only view onto the *authoritative* `geodb.user_states` collection."""
from os import getenv
from app import cfg

from pymongo import MongoClient

client = MongoClient(getenv("MONGO_URI", "mongodb://mongo:27017"), tz_aware=True)
user_states = client["geodb"]["user_states"]