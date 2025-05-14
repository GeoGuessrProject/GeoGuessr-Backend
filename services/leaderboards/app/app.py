# app.py
from flask import Flask, request, jsonify
from datetime import datetime

# Mock in-memory database
scores = []

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    @app.post("/submit")
    def submit():
        data = request.get_json()
        if not data:
            return {"error": "JSON required"}, 400
        # Upsert logic for in-memory database
        for score in scores:
            if score["username"] == data["username"]:
                score.update({
                    "email": data["email"],
                    "score": data["score"],
                    "ts": datetime.now()
                })
                break
        else:
            scores.append({
                "username": data["username"],
                "email": data["email"],
                "score": data["score"],
                "ts": datetime.now()
            })
        # Sort in-memory database
        scores.sort(key=lambda x: (-x["score"], x["ts"]))
        return {"ok": True}, 201

    @app.get("/top10")
    def top10():
        # Get the top 10 scores sorted by score (descending) and timestamp (ascending)
        top = sorted(scores, key=lambda x: (-x["score"], x["ts"]))[:10]
        # Hide email before returning to clients
        for doc in top:
            doc.pop("email", None)
        return jsonify(top)

    if __name__ == "__main__":
        app.run(debug=True)