# Review Analytics API

A FastAPI application with Celery for async tasks, PostgreSQL for data storage, and Redis for task queueing. Provides review trend analysis and paginated review access with AI-powered sentiment analysis.

## Features

- ✨ AI-powered review analysis using GPT-4
- 📊 Review trends and analytics
- 🔄 Asynchronous task processing with Celery
- 🗄️ PostgreSQL database for data persistence
- 🚀 Fast API endpoints with async support
- 🔍 Sentiment and tone analysis for reviews
- 📝 Comprehensive review history tracking

## Technologies

- **API Server**: FastAPI
- **Database**: PostgreSQL
- **Task Queue**: Celery + Redis
- **AI Integration**: OpenAI GPT

## Prerequisites

- Python 3.8+
- PostgreSQL
- Redis
- OpenAI API key

## Installation

1. Clone the repository:

```bash
git clone https://github.com/mehul100100/fastapi-review-analyzer.git
cd fastapi-review-analyzer
```

2. Copy the .env.example file to .env and fill in the missing values:

```bash
cp .env.example .env    
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```
3. Create a new database named 'reviews'


```bash
psql -U postgres -c "CREATE DATABASE reviews;"
```

4. Run Alembic migrations:

```bash
alembic init alembic
```

Update `alembic/env.py` with the correct database URL configuration:

```python
from app.models import Base
from app.config import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Update this line with your database URL
database_url = f"postgresql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST_NAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
config.set_main_option(
    "sqlalchemy.url", 
    database_url
)

target_metadata = Base.metadata
```

```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

5. Run the celery worker:

```bash
celery -A app.tasks worker --loglevel=info
```
6. Populate the database with some sample data:

```bash
python3 insert_test_data.py
```

7. Run the FastAPI server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```