from celery import Celery
from app.core.config import REDIS_URL

celery_app = Celery(
    "sentinelstream",
    broker=REDIS_URL,
    backend=REDIS_URL
)
