from app.schemas.book import BookRead,BookCreate , BookUpdate
from abc import ABC, abstractmethod
from typing import List, Optional

class BookRepository(ABC):
    @abstractmethod
    def create_book(self, book: BookCreate) -> BookRead:
        """Create a new book."""
        pass

    @abstractmethod
    def get_book_by_id(self, book_id: int) -> Optional[BookRead]:
        """Get a book by its ID."""
        pass

    @abstractmethod
    def get_all_books(self) -> List[BookRead]:
        """Get all books."""
        pass

    @abstractmethod
    def update_book(self, book_id: int, book: BookUpdate) -> Optional[BookUpdate]:
        """Update an existing book."""
        pass

    @abstractmethod
    def delete_book(self, book_id: int) -> bool:
        """Delete a book by its ID."""
        pass