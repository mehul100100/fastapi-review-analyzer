from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, func, Index
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    reviews = relationship('ReviewHistory', back_populates='category')

class ReviewHistory(Base):
    __tablename__ = 'reviewhistory'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=True)
    stars = Column(Integer, nullable=False)
    review_id = Column(String(255), nullable=False)
    tone = Column(String(255), nullable=True)
    sentiment = Column(String(255), nullable=True)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    category = relationship('Category', back_populates='reviews')

Index('idx_reviewhistory_review_id', ReviewHistory.review_id)
Index('idx_reviewhistory_created_at', ReviewHistory.created_at)
Index('idx_reviewhistory_category_id', ReviewHistory.category_id)

class AccessLog(Base):
    __tablename__ = 'accesslog'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())