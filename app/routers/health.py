from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.core.celery_app import celery_app

router = APIRouter()

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    status = {"status": "ok", "db": "unknown", "redis": "unknown"}

    try:
        db.execute(text("SELECT 1"))
        status["db"] = "ok"
    except Exception as e:
        status["db"] = f"error: {str(e)}"
        status["status"] = "degraded"

    try:
        celery_app.backend.client.ping()
        status["redis"] = "ok"
    except Exception as e:
        status["redis"] = f"error: {str(e)}"
        status["status"] = "degraded"

    return status
