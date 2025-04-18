from fastapi import FastAPI, Request
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

@app.post("/user/{username}/guess")
async def make_guess(username: str, request: Request):
    data = await request.json()
    guess = data.get("guess", "").strip().lower()

    user = user_states.find_one({"username": username})
    if not user or "current_game" not in user:
        return {"error": "Game not found for user"}

    correct = guess == "paris"
    score_delta = 100 if correct else 0

    # Update current_game
    user_states.update_one(
        {"username": username},
        {
            "$inc": {"current_game.score": score_delta, "current_game.round": 1},
            "$push": {"current_game.location_history": {"guess": guess, "correct": correct}}
        }
    )

    return {"correct": correct, "message": "Guess received"}

@app.post("/user/{username}/end-game")
def end_game(username: str):
    user = user_states.find_one({"username": username})
    if not user or "current_game" not in user or not user["current_game"]:
        return {"error": "No game in progress"}

    game = user["current_game"]
    game["end_time"] = datetime.now(timezone.utc)

    # Push current game to history
    result = user_states.update_one(
        {"username": username},
        {
            "$push": {"history": game},
            "$set": {
                "current_game": {
                    "score": 0,
                    "round": 0,
                    "location_history": [],
                    "start_time": None,
                    "end_time": None
                }
            }
        }
    )

    if result.matched_count == 0:
        return {"error": "User not found"}

    return {"message": "Game ended and saved to history."}

# Start listening to RabbitMQ events
start_consumer_thread()
