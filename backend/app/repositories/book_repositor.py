from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate, BookRead
from app.interfaces.Ibook_repository import BookRepository

class RepoBook(BookRepository):
    def __init__(self, db: Session):
        self.db = db

    def create_book(self, book: BookCreate) -> BookRead:
        """Crea un libro. Lanza ValueError si el título ya existe."""
        try:
            if self.db.query(Book).filter(Book.title == book.title).first():
                raise ValueError("El título ya existe")

            db_book = Book(**book.dict())
            self.db.add(db_book)
            self.db.commit()
            self.db.refresh(db_book)
            return BookRead.from_orm(db_book)
        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"Error creando un libro: {e}")
            raise e

    def get_book_by_id(self, book_id: int) -> Optional[BookRead]:
        """Obtiene un libro por ID. Devuelve None si no existe."""
        try:
            db_book = self.db.query(Book).filter(Book.id == book_id).first()
            if db_book:
                return BookRead.from_orm(db_book)
            return None
        except SQLAlchemyError as e:
            raise e

    def get_all_books(self) -> List[BookRead]:
        """Obtiene todos los libros."""
        try:
            books = self.db.query(Book).all()
            return [BookRead.from_orm(book) for book in books]
        except SQLAlchemyError as e:
            raise e

    def update_book(self, book_id: int, book_update: BookUpdate) -> Optional[BookRead]:
        """Actualiza un libro. Devuelve None si no existe."""
        try:
            db_book = self.db.query(Book).filter(Book.id == book_id).first()
            if not db_book:
                return None

            for key, value in book_update.dict(exclude_unset=True).items():
                setattr(db_book, key, value)
            
            self.db.commit()
            self.db.refresh(db_book)
            return BookRead.from_orm(db_book)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def delete_book(self, book_id: int) -> bool:
        """Elimina un libro. Devuelve False si no existe."""
        try:
            db_book = self.db.query(Book).filter(Book.id == book_id).first()
            if not db_book:
                return False

            self.db.delete(db_book)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e