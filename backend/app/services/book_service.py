from typing import List, Optional
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate
from app.repositories.book_repositor import RepoBook

class BookService:
    def __init__(self, book_repo):
        self.book_repo = book_repo

    async def create_book(self, book_data: BookCreate) -> Book:
        existing_book = await self.book_repo.get_book_by_title(book_data.title)
        if existing_book:
            raise ValueError("El título ya existe")
        return await self.book_repo.create_book(book_data)

    async def get_book(self, book_id: int) -> Optional[Book]:
        return await self.book_repo.get_book_by_id(book_id)

    async def get_all_books(self, skip: int = 0, limit: int = 10) -> List[Book]:
        return await self.book_repo.get_all_books(skip, limit)

    async def get_books_by_category(self, category: str, skip: int = 0, limit: int = 10) -> List[Book]:
        return await self.book_repo.get_books_by_category(category, skip, limit)

    async def search_books(self, search_term: str, skip: int = 0, limit: int = 10) -> List[Book]:
        return await self.book_repo.search_books(search_term, skip, limit)

    async def update_book(self, book_id: int, book_data: BookUpdate) -> Optional[Book]:
        return await self.book_repo.update_book(book_id, book_data)

    async def delete_book(self, book_id: int) -> bool:
        return await self.book_repo.delete_book(book_id)
