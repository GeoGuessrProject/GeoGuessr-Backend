# top10.py

from datetime import datetime

# this will be set by process_event so main.py can pick it up
latest_top10 = []

def process_event(evt, user_states, load_prev):
    """
    evt: {username, email, score, end_time}
    user_states: pymongo collection
    load_prev: fn() -> [prev_top10_usernames]
    """
    player   = evt["username"]
    prev     = set(load_prev())

    # recompute current top10
    docs = list(
      user_states
        .find({}, {
           "username":1,
           "email":1,
           "total_score":1,
           "last_end_time":1
        })
        .sort([
           ("total_score", -1),
           ("last_end_time", 1)
        ])
        .limit(10)
    )
    new_top10 = [d["username"] for d in docs]
    global latest_top10
    latest_top10 = new_top10

    # did player newly enter?
    if player in new_top10 and player not in prev:
        # who dropped?
        dropped = [u for u in prev if u not in new_top10]
        emails = []
        for victim in dropped:
            vdoc = user_states.find_one({"username": victim})
            subject = "You fell out of the Top 10!"
            body    = (
              f"Hi {victim},\n\n"
              f"Your score of {vdoc['total_score']} was just overtaken—you’re now #11.\n"
              "Time for a rematch!\n\n— The Team"
            )
            emails.append((vdoc["email"], subject, body))
        return emails

    return []
