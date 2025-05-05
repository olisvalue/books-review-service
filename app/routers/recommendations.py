from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.dependencies import get_db
from app.models import Book, Review

router = APIRouter()

@router.get("/recommendations")
def get_recommendations(db: Session = Depends(get_db)):
    book_stats = (
        db.query(
            Review.book_id,
            func.count(Review.id).label("num_reviews"),
            func.avg(Review.rating).label("avg_rating"),
        )
        .group_by(Review.book_id)
        .subquery()
    )

    recommendations = (
        db.query(
            Book,
            (
                book_stats.c.avg_rating
                * book_stats.c.num_reviews
                / (book_stats.c.num_reviews + 10)
            ).label("score"),
        )
        .join(book_stats, Book.id == book_stats.c.book_id)
        .filter(book_stats.c.num_reviews >= 3)
        .order_by(desc("score"))
        .limit(5)
        .all()
    )

    return {
        "recommendations": [
            {"id": book.id, "title": book.title, "author": book.author}
            for book, _score in recommendations
        ]
    }
