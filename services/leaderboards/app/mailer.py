import smtplib
import ssl
from email.message import EmailMessage

from app import cfg
import logging

def send_fallen_email(username: str, email: str, last_rank: int):
    """Send the polite heads‑up. Exceptions are swallowed but logged."""
    msg = EmailMessage()
    msg["Subject"] = "Heads‑up: you’ve left the Top 10!"
    msg["From"]    = cfg.FROM_ADDR
    msg["To"]      = email
    msg.set_content(
        f"Hi {username},\n\n"
        f"You were just bumped to rank {last_rank}. "
        "Tighten those reflexes and get back in there!\n\n"
        "— Your Friendly Leaderboard Bot"
    )

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(cfg.MAIL_HOST, cfg.MAIL_PORT, timeout=10) as s:
            s.starttls(context=context)
            s.login(cfg.MAIL_USER, cfg.MAIL_PASS)
            s.send_message(msg)
    except smtplib.SMTPException as exc:
        logging.exception(f"[MAILER] Failed to send e‑mail to {email}: {exc}")
        print(f"[MAILER] Failed to send e‑mail to {email}: {exc}")