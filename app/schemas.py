from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class CategoryTrend(BaseModel):
    id: int
    name: str
    description: Optional[str]
    average_stars: float
    total_reviews: int

class ReviewResponse(BaseModel):
    id: int
    text: Optional[str]
    stars: int
    review_id: str
    created_at: datetime
    tone: Optional[str]
    sentiment: Optional[str]
    category_id: int

class ReviewListResponse(BaseModel):
    data: List[ReviewResponse]
    next_cursor: Optional[str]