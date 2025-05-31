from app.schemas.book import BookRead,BookCreate , BookUpdate
from abc import ABC, abstractmethod
from typing import List, Optional

class BookRepository(ABC):
    @abstractmethod
    def create_book(self, book: BookCreate) -> BookRead:
        pass

    @abstractmethod
    def get_book_by_id(self, book_id: int) -> Optional[BookRead]:
        pass

    @abstractmethod
    def get_all_books(self) -> List[BookRead]:
        pass

    @abstractmethod
    def update_book(self, book_id: int, book: BookUpdate) -> Optional[BookUpdate]:
        pass

    @abstractmethod
    def delete_book(self, book_id: int) -> bool:
        pass