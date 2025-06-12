from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.user_likes_repository import LikeRepository
from app.repositories.user_repository import UserRepository
from app.repositories.book_repositor import BookRepository
from app.models.book import Book
from app.models.user import User

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

    async def add_like(self, user_id: int, book_id: int) -> bool:
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
        
        book = await self.book_repo.get_book_by_id(book_id)
        if not book:
            raise ValueError("Libro no encontrado")

        return await self.like_repo.add_like(user_id, book_id)

    async def remove_like(self, user_id: int, book_id: int) -> bool:
        return await self.like_repo.remove_like(user_id, book_id)

    async def get_user_likes(self, user_id: int) -> List[int]:
        return await self.like_repo.get_user_likes(user_id)

    async def count_likes_for_book(self, book_id: int) -> int:
        return await self.like_repo.count_likes_for_book(book_id)