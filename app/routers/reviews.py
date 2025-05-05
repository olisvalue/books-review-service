from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Review, User, Book  
from ..schemas import ReviewCreate, ReviewResponse
from ..dependencies import get_current_user

router = APIRouter()

@router.post("/reviews", response_model=ReviewResponse)
def create_review(
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        db_book = db.query(Book).filter(Book.id == review.book_id).first()
        if not db_book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        db_review = Review(
            rating=review.rating,
            comment=review.comment,
            user_id=current_user.id,
            book_id=review.book_id
        )
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        
        return {
            "id": db_review.id,
            "rating": db_review.rating,
            "comment": db_review.comment,
            "book_id": db_review.book_id,
            "username": current_user.username
        }
    
    except Exception:
        raise HTTPException(...)