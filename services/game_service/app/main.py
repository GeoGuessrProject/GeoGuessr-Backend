import os, json, pika
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.message_handler import start_consumer_thread
from app.db import user_states
from app.game_logic import get_user, start_game_for_user, update_guess, end_game_for_user

app = FastAPI()

AMQP_URL    = os.getenv("AMQP_URL")
TOP10_QUEUE = "top10-notify"

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
    result = start_game_for_user(username)
    if result.matched_count == 0:
        return {"error": "User not found"}
    return {"message": "Game started"}

@app.post("/user/{username}/guess")
async def make_guess(username: str, request: Request):
    data = await request.json()
    guess = data.get("guess", "")
    correct_answer = data.get("correctAnswer", "")
    correct = update_guess(username, guess, correct_answer)
    return {"correct": correct, "message": "Guess processed"}


@app.post("/user/{username}/end-game")
def end_game(username: str):

    result = end_game_for_user(username)

    client_msg = {"message": result["message"]}

     # RabbitMQ payload
    payload = {
        "username": result["username"],
        "email":    result["email"],
        "score":    result["new_score"],
        "end_time": result["end_time"],
    }

    conn    = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
    channel = conn.channel()
    channel.queue_declare(queue=TOP10_QUEUE, durable=True)
    channel.basic_publish(
        exchange="",
        routing_key=TOP10_QUEUE,
        body=json.dumps(payload),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    conn.close()

    return client_msg

@app.on_event("startup")
def startup_event():
    start_consumer_thread()
