from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from backend.app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate
from backend.app.interfaces.Ireview_repository import IReviewRepository

class ReviewRepository(IReviewRepository):
    def __init__(self, db: Session):
        self.db = db

    def create_review(self, review: ReviewCreate) -> Review:
        try:
            db_review = Review(**review.dict())
            self.db.add(db_review)
            self.db.commit()
            self.db.refresh(db_review)
            return db_review
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def get_review_by_id(self, review_id: int) -> Optional[Review]:
        return self.db.query(Review).filter(Review.id == review_id).first()

    def get_reviews_by_book(self, book_id: int) -> List[Review]:
        return self.db.query(Review).filter(Review.book_id == book_id).all()

    def get_reviews_by_user(self, user_id: int) -> List[Review]:
        return self.db.query(Review).filter(Review.user_id == user_id).all()

    def update_review(self, review_id: int, review_update: ReviewUpdate) -> Optional[Review]:
        try:
            db_review = self.db.query(Review).filter(Review.id == review_id).first()
            if not db_review:
                return None

            for key, value in review_update.dict(exclude_unset=True).items():
                setattr(db_review, key, value)

            self.db.commit()
            self.db.refresh(db_review)
            return db_review
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def delete_review(self, review_id: int) -> bool:
        try:
            db_review = self.db.query(Review).filter(Review.id == review_id).first()
            if not db_review:
                return False

            self.db.delete(db_review)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e