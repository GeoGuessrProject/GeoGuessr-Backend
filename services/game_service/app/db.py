import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
mongo_client = MongoClient(mongo_uri, server_api=ServerApi('1'))
    
db = mongo_client["geodb"]
user_states = db["user_states"]
