from abc import ABC, abstractmethod
from typing import List, Optional
from backend.app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate

class IReviewRepository(ABC):
    @abstractmethod
    def create_review(self, review: ReviewCreate) -> Review:
        pass

    @abstractmethod
    def get_review_by_id(self, review_id: int) -> Optional[Review]:
        pass

    @abstractmethod
    def get_reviews_by_book(self, book_id: int) -> List[Review]:
        pass

    @abstractmethod
    def get_reviews_by_user(self, user_id: int) -> List[Review]:
        pass

    @abstractmethod
    def update_review(self, review_id: int, review_update: ReviewUpdate) -> Optional[Review]:
        pass

    @abstractmethod
    def delete_review(self, review_id: int) -> bool:
        pass