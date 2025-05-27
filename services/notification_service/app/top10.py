# top10.py
from datetime import datetime

def process_event(evt, user_states, load_prev):
    """
    Returns (emails, new_top10_usernames)
    emails: List of (to, subject, body) tuples
    new_top10_usernames: list of the current top-10 usernames
    """
    player = evt["username"]
    prev   = set(load_prev())

    # Recompute the current top 10
    docs = list(
        user_states
          .find({}, {"username":1, "email":1, "total_score":1, "last_end_time":1})
          .sort([("total_score",-1),("last_end_time",1)])
          .limit(10)
    )
    new_top10 = [d["username"] for d in docs]

    emails = []
    # Did someone new enter?
    if player in new_top10 and player not in prev:
        dropped = [u for u in prev if u not in new_top10]
        for victim in dropped:
            vdoc    = user_states.find_one({"username": victim})
            subject = "You fell out of the Top 10!"
            body    = (
              f"Hi {victim},\n\n"
              f"Your score of {vdoc['total_score']} was just overtaken—you’re now off the Top-10.\n"
              "Time to rematch!\n\n— The Team"
            )
            emails.append((vdoc["email"], subject, body))

    return emails, new_top10
