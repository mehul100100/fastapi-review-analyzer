from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Category, ReviewHistory
from datetime import datetime, timedelta

def insert_test_data():
    db: Session = SessionLocal()
    
    # Insert Categories
    categories = [
        Category(name="Electronics", description="Gadgets and electronic devices"),
        Category(name="Books", description="Books across all genres"),
        Category(name="Home & Kitchen", description="Home appliances and kitchenware"),
        Category(name="Fashion", description="Clothing and accessories"),
        Category(name="Sports", description="Sports equipment and gear"),
        Category(name="Beauty", description="Cosmetics and personal care"),
        Category(name="Toys", description="Games and toys"),
        Category(name="Automotive", description="Car parts and accessories"),
        Category(name="Garden", description="Garden tools and plants"),
        Category(name="Pet Supplies", description="Products for pets")
    ]
    
    db.add_all(categories)
    db.commit()

    # Sample reviews for each category
    reviews_data = {
        "Electronics": [
            ("Amazing smartphone, great camera!", 9),
            ("Battery life could be better", 6),
            ("Perfect laptop for work", 8),
            ("Headphones broke after a month", 3),
            ("Great value for money", 7)
        ],
        "Books": [
            ("Couldn't put it down!", 9),
            ("Interesting plot but slow pacing", 6),
            ("Best book I've read this year", 10),
            ("Not what I expected", 5),
            ("Great author, great book", 8)
        ],
        "Home & Kitchen": [
            ("Works perfectly for my needs", 8),
            ("Good quality blender", 7),
            ("Stopped working after 2 months", 4),
            ("Best coffee maker ever", 9),
            ("Decent product for the price", 6)
        ],
        "Fashion": [
            ("Perfect fit and style", 9),
            ("Material quality is poor", 4),
            ("Love these shoes!", 8),
            ("Sizing runs small", 5),
            ("Great winter coat", 7)
        ],
        "Sports": [
            ("Excellent running shoes", 9),
            ("Good gym equipment", 7),
            ("Durable tennis racket", 8),
            ("Comfortable workout gear", 8),
            ("Perfect for beginners", 7)
        ],
        "Beauty": [
            ("Great results, will buy again", 9),
            ("Caused slight irritation", 4),
            ("Love this product", 8),
            ("Too expensive for what it is", 5),
            ("Amazing fragrance", 8)
        ],
        "Toys": [
            ("Kids love it!", 9),
            ("Good educational value", 8),
            ("Broke easily", 3),
            ("Hours of fun", 8),
            ("Better than expected", 7)
        ],
        "Automotive": [
            ("Perfect fit for my car", 8),
            ("Easy installation", 7),
            ("Good quality parts", 8),
            ("Bit pricey but worth it", 7),
            ("Works as advertised", 7)
        ],
        "Garden": [
            ("Great garden tools", 8),
            ("Plants arrived healthy", 9),
            ("Excellent pruning shears", 7),
            ("Seeds germinated well", 8),
            ("Durable garden hose", 7)
        ],
        "Pet Supplies": [
            ("My dog loves this toy", 9),
            ("Good quality pet food", 8),
            ("Perfect size bed for my cat", 8),
            ("Durable leash", 7),
            ("Great value pet supplies", 8)
        ]
    }

    # Insert reviews for each category
    for idx, category in enumerate(categories):
        reviews = []
        category_reviews = reviews_data[category.name]
        
        for review_idx, (text, stars) in enumerate(category_reviews):
            # Create reviews with different timestamps
            created_at = datetime.utcnow() - timedelta(days=review_idx)
            review = ReviewHistory(
                text=text,
                stars=stars,
                review_id=f"rev_{category.id}_{review_idx}",
                category_id=category.id,
                created_at=created_at
            )
            reviews.append(review)
        
        db.add_all(reviews)
    
    db.commit()
    db.close()
    
    print("Test data inserted successfully!")

if __name__ == "__main__":
    insert_test_data()
