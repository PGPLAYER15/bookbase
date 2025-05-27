from typing import List, Optional
from app.models import Book
from app.schemas import BookCreate, BookUpdate
from app.repositories import BookRepository

class BookService:
    def __init__(self, book_repo: BookRepository):
        self.book_repo = book_repo

    def create_book(self, book_data: BookCreate) -> Book:
        existing_book = self.book_repo.get_book_by_title(book_data.title)
        if existing_book:
            raise ValueError("El título ya existe")
        return self.book_repo.create_book(book_data)

    def get_book(self, book_id: int) -> Optional[Book]:
        return self.book_repo.get_book_by_id(book_id)

    def get_all_books(self) -> List[Book]:
        return self.book_repo.get_all_books()

    def update_book(self, book_id: int, book_data: BookUpdate) -> Optional[Book]:
        return self.book_repo.update_book(book_id, book_data)

    def delete_book(self, book_id: int) -> bool:
        return self.book_repo.delete_book(book_id)