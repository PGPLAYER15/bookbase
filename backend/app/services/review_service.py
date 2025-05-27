from typing import List, Optional
from backend.app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate
from backend.app.interfaces.Ireview_repository import IReviewRepository

class ReviewService:
    def __init__(self, review_repo: IReviewRepository):
        self.review_repo = review_repo

    def create_review(self, review_data: ReviewCreate) -> Review:
        """Crea una reseña con validación de usuario/libro existente"""
        return self.review_repo.create_review(review_data)

    def get_review(self, review_id: int) -> Optional[Review]:
        """Obtiene una reseña por ID"""
        return self.review_repo.get_review_by_id(review_id)

    def get_book_reviews(self, book_id: int) -> List[Review]:
        """Obtiene todas las reseñas de un libro"""
        return self.review_repo.get_reviews_by_book(book_id)

    def get_user_reviews(self, user_id: int) -> List[Review]:
        """Obtiene todas las reseñas de un usuario"""
        return self.review_repo.get_reviews_by_user(user_id)

    def update_review(self, review_id: int, review_data: ReviewUpdate) -> Optional[Review]:
        """Actualiza una reseña existente"""
        return self.review_repo.update_review(review_id, review_data)

    def delete_review(self, review_id: int) -> bool:
        """Elimina una reseña"""
        return self.review_repo.delete_review(review_id)