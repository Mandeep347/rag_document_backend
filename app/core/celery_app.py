from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.redis_url+"0",
    backend=settings.redis_url+"0",
    include=["app.tasks.ingestion_tasks"],
)

import app.models