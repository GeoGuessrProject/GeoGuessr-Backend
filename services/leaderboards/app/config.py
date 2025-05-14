import os
from functools import lru_cache

class Config:
    """Central settings object, read once per process."""
    mongo_uri: str
    redis_host: str
    smtp_user: str
    smtp_pass: str
    broker_url: str

    def __init__(self) -> None:
        self.mongo_uri  = os.getenv("MONGO_URI", "mongodb://mongo:27017/geo")
        self.redis_host = os.getenv("REDIS_HOST", "redis")
        self.smtp_user  = os.getenv("MAIL_USER")
        self.smtp_pass  = os.getenv("MAIL_PASS")
        # Celery broker (RabbitMQ)
        rb_user = os.getenv("RABBITMQ_USER", "guest")
        rb_pass = os.getenv("RABBITMQ_PASS", "guest")
        rb_host = os.getenv("RABBITMQ_HOST", "rabbitmq")
        self.broker_url = f"amqp://{rb_user}:{rb_pass}@{rb_host}//"

@lru_cache
def ConfigSingleton() -> Config:                # optional helper
    return Config()
