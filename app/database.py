from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import time

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST_NAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
def create_engine_with_retry(url, retries=5, delay=3):
    for i in range(retries):
        try:
            return create_engine(url)
        except OperationalError:
            if i < retries - 1:
                time.sleep(delay)
                continue
            raise


engine = create_engine_with_retry(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()