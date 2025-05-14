from __future__ import annotations
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
import os
from functools import cached_property


class Config:  # pylint: disable=too-few-public-methods
    """Read‑only settings, pulled once at import time."""

    # ----- raw env‑vars --------------------------------------------------
    _mongo_uri: str = os.getenv("MONGO_URI", "mongodb://mongo:27017/geo")
    _redis_host: str = os.getenv("REDIS_HOST", "redis")
    _smtp_user: str | None = os.getenv("MAIL_USER")
    _smtp_pass: str | None = os.getenv("MAIL_PASS")
    _rb_user: str = os.getenv("RABBITMQ_USER", "guest")
    _rb_pass: str = os.getenv("RABBITMQ_PASS", "guest")
    _rb_host: str = os.getenv("RABBITMQ_HOST", "rabbitmq")

    # ----- public helpers ------------------------------------------------
    @property
    def mongo_uri(self) -> str:  # noqa: D401 – simple getters are fine
        return self._mongo_uri

    @property
    def redis_host(self) -> str:
        return self._redis_host

    @property
    def smtp_user(self) -> str | None:
        return self._smtp_user

    @property
    def smtp_pass(self) -> str | None:
        return self._smtp_pass

    @cached_property
    def broker_url(self) -> str:
        """Celery broker string, constructed lazily once."""
        return f"amqp://{self._rb_user}:{self._rb_pass}@{self._rb_host}//"