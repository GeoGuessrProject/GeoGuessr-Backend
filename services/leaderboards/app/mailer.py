from __future__ import annotations

import logging
import smtplib
from email.message import EmailMessage

from app import cfg

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

LOGGER = logging.getLogger(__name__)


def send_fallen_email(to_addr: str, username: str, old_rank: int) -> None:
    """Send a polite notice that *username* is no longer in Top 10."""
    if not cfg.smtp_user or not cfg.smtp_pass:
        LOGGER.warning("Mail credentials missing – skipping email to %s", to_addr)
        return

    msg = EmailMessage()
    msg["Subject"] = "You just fell out of GeoGuessr Top 10 🙁"
    msg["From"] = cfg.smtp_user
    msg["To"] = to_addr
    msg.set_content(
        (
            f"Hi {username},\n\n"  # noqa: E501
            "Another player just overtook your score, pushing you to rank "
            f"{old_rank + 1}. Time to play another round and reclaim your spot!\n\n"
            "Have fun,\nGeoGuessr‑Team"
        )
    )

    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(cfg.smtp_user, cfg.smtp_pass)
            server.send_message(msg)
            LOGGER.info("Notification mail sent to %s", to_addr)
    except Exception as exc:  # pylint: disable=broad-except
        LOGGER.exception("Failed to send e‑mail to %s: %s", to_addr, exc)