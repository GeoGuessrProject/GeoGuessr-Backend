

db.scores.create_index([("score", pymongo.DESCENDING),
                        ("created_at", pymongo.ASCENDING)])


top10 = list(
    db.scores.find()
             .sort([("score", -1), ("created_at", 1)])  # score ↓, oldest first
             .limit(10)
)