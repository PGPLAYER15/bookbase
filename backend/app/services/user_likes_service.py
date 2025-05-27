from typing import List, Optional
from sqlalchemy.orm import Session
from backend.app.repositories.user_likes_repository import LikeRepository
from backend.app.repositories.user_repository import UserRepository
from backend.app.repositories.book_repositor import BookRepository
from app.models import User, Book

class LikeService:
    def __init__(
        self,
        like_repo: LikeRepository,
        user_repo: UserRepository,
        book_repo: BookRepository
    ):
        self.like_repo = like_repo
        self.user_repo = user_repo
        self.book_repo = book_repo

    def add_like(self, user_id: int, book_id: int) -> bool:

        if not self.user_repo.get_user_by_id(user_id):
            raise ValueError("Usuario no encontrado")
        if not self.book_repo.get_book_by_id(book_id):
            raise ValueError("Libro no encontrado")

        return self.like_repo.add_like(user_id, book_id)

    def remove_like(self, user_id: int, book_id: int) -> bool:
        return self.like_repo.remove_like(user_id, book_id)

    def get_user_likes(self, user_id: int) -> List[Book]:
        book_ids = self.like_repo.get_user_likes(user_id)
        return [self.book_repo.get_book_by_id(book_id) for book_id in book_ids]

    def count_likes_for_book(self, book_id: int) -> int:
        return self.like_repo.count_likes_for_book(book_id)