from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas, tasks
from .database import get_db
from datetime import datetime
from typing import Optional, List
from openai import OpenAI
import json
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)
app = FastAPI()

def analyze_review(text: str, stars: int) -> dict:
    prompt = f"""
    Analyze the following review for tone and sentiment.
    Review Text: "{text}"
    Star Rating: {stars}/10
    Provide the tone (e.g., formal, informal, positive, negative, neutral) and sentiment (positive, negative, neutral).
    Respond with JSON.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        result = json.loads(response.choices[0].message.content)
        return {
            "tone": result.get("tone"),
            "sentiment": result.get("sentiment")
        }
    except Exception as e:
        print(f"Error analyzing review: {e}")
        return {"tone": None, "sentiment": None}

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/log-test/")
async def test_log():
    tasks.log_access.delay("Test log entry")
    return {"message": "Log entry queued"}

@app.get("/reviews/trends", response_model=List[schemas.CategoryTrend])
async def get_review_trends(db: Session = Depends(get_db)):
    # Subquery to get latest reviews per review_id
    subquery = (
        db.query(
            models.ReviewHistory.review_id,
            func.max(models.ReviewHistory.created_at).label('max_created_at')
        )
        .group_by(models.ReviewHistory.review_id)
        .subquery()
    )

    # Join with Category and aggregate
    trends = (
        db.query(
            models.Category.id,
            models.Category.name,
            models.Category.description,
            func.avg(models.ReviewHistory.stars).label('average_stars'),
            func.count(models.ReviewHistory.id).label('total_reviews')
        )
        .join(subquery, models.ReviewHistory.review_id == subquery.c.review_id)
        .join(models.Category)
        .filter(models.ReviewHistory.created_at == subquery.c.max_created_at)
        .group_by(models.Category.id)
        .order_by(func.avg(models.ReviewHistory.stars).desc())
        .limit(5)
        .all()
    )

    # Format response
    response = [
        {
            "id": cat_id,
            "name": name,
            "description": desc,
            "average_stars": round(avg, 2),
            "total_reviews": total
        } for cat_id, name, desc, avg, total in trends
    ]

    # Log access
    tasks.log_access.delay("GET /reviews/trends")

    return response

@app.get("/reviews/", response_model=schemas.ReviewListResponse)
async def get_reviews(
    category_id: int,
    cursor: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    page_size = 15

    # Get latest reviews per review_id in category
    subquery = (
        db.query(
            models.ReviewHistory.review_id,
            func.max(models.ReviewHistory.created_at).label('max_created_at')
        )
        .filter(models.ReviewHistory.category_id == category_id)
        .group_by(models.ReviewHistory.review_id)
        .subquery()
    )

    query = (
        db.query(models.ReviewHistory)
        .join(
            subquery,
            (models.ReviewHistory.review_id == subquery.c.review_id) &
            (models.ReviewHistory.created_at == subquery.c.max_created_at)
        )
        .filter(models.ReviewHistory.category_id == category_id)
    )

    if cursor:
        query = query.filter(models.ReviewHistory.created_at < cursor)

    reviews = query.order_by(models.ReviewHistory.created_at.desc()).limit(page_size).all()

    # Compute tone/sentiment if missing
    for review in reviews:
        # print(f"Processing review ID: {review.id}, Text: {review.text[:50]}...")
        if review.tone is None or review.sentiment is None:
            # print(f"Missing tone/sentiment for review {review.id}, analyzing...")
            analysis = analyze_review(review.text, review.stars)
            # print(f"Analysis results - Tone: {analysis['tone']}, Sentiment: {analysis['sentiment']}")
            review.tone = analysis['tone']
            review.sentiment = analysis['sentiment']
            db.commit()
            # print(f"Updated review {review.id} with tone and sentiment")

    # Prepare response
    response_data = [
        {
            "id": review.id,
            "text": review.text,
            "stars": review.stars,
            "review_id": review.review_id,
            "created_at": review.created_at,
            "tone": review.tone,
            "sentiment": review.sentiment,
            "category_id": review.category_id
        } for review in reviews
    ]

    next_cursor = reviews[-1].created_at if reviews else None

    # Log access
    tasks.log_access.delay(f"GET /reviews/?category_id={category_id}")

    return {
        "data": response_data,
        "next_cursor": next_cursor.isoformat() if next_cursor else None
    }