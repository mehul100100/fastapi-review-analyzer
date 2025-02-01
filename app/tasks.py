from celery import Celery
from .database import SessionLocal
from .models import AccessLog
import os

celery_app = Celery(
    'tasks',
    broker=os.getenv("REDIS_URL", "redis://localhost:6379"),
    backend=os.getenv("REDIS_BACKEND_URL", "redis://localhost:6379")
)

@celery_app.task
def log_access(text: str):
    db = SessionLocal()
    try:
        access_log = AccessLog(text=text)
        db.add(access_log)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()