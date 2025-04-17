from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from message_handler import start_consumer_thread, user_states
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {"message": "Connected"}

@app.get("/user/{username}/profile")
def get_user_profile(username: str):
    user = user_states.find_one({"username": username}, {"_id": 0})
    if not user:
        return {"error": "User not found"}
    return user

@app.post("/user/{username}/start-game")
def start_game(username: str):
    result = user_states.update_one(
        {"username": username},
        {
            "$set": {
                "current_game": {
                    "score": 0,
                    "round": 1,
                    "location_history": [],
                    "start_time": datetime.now(timezone.utc),
                    "end_time": None
                }
            },
            "$inc": {"games_played": 1}
        }
    )
    if result.matched_count == 0:
        return {"error": "User not found"}
    return {"message": "Game started"}


# Start listening to RabbitMQ events
start_consumer_thread()
