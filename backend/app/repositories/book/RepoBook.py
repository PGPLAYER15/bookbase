from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.book.book import Book
from app.schemas.book import BookCreate, BookUpdate, BookRead
from app.repositories.book.IRepoBook import BookRepository

class RepoBook(BookRepository):
    
    def __init__(self, db: Session):
        self.db = db

    def create_book(self, book: BookCreate) -> BookRead:
        db_book = Book(**book.dict())
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book

    def get_book_by_id(self, book_id: int) -> Optional[BookRead]:
        return self.db.query(Book).filter(Book.id == book_id).first()

    def get_all_books(self) -> List[BookRead]:
        return self.db.query(Book).all()

    def update_book(self, book_id: int, book_update: BookUpdate) -> Optional[BookRead]:
        db_book = self.db.query(Book).filter(Book.id == book_id).first()
        if not db_book:
            return None
        for key, value in book_update.dict(exclude_unset=True).items():
            setattr(db_book, key, value)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book

    def delete_book(self, book_id: int) -> bool:
        db_book = self.db.query(Book).filter(Book.id == book_id).first()
        if not db_book:
            return False
        self.db.delete(db_book)
        self.db.commit()
        return True