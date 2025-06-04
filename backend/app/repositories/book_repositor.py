from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate, BookRead
from app.interfaces.Ibook_repository import BookRepository

class RepoBook(BookRepository):
    def __init__(self, db):
        self.db = db

    async def create_book(self, book: BookCreate) -> BookRead:
        try:
            result = await self.db.execute(
                select(Book).where(Book.title == book.title)
            )
            if result.scalars().first():
                raise ValueError("El título ya existe")

            book_dict = book.dict()
            book_dict["link"] = str(book_dict["link"])  # <-- Convierte HttpUrl a str

            db_book = Book(**book_dict)
            self.db.add(db_book)
            await self.db.commit()
            await self.db.refresh(db_book)
            return BookRead.from_orm(db_book)
        except SQLAlchemyError as e:
            await self.db.rollback()
            print(f"Error creando un libro: {e}")
            raise e

    async def get_book_by_id(self, book_id: int) -> Optional[BookRead]:
        try:
            result = await self.db.execute(
                select(Book).where(Book.id == book_id)
            )
            db_book = result.scalars().first()
            if db_book:
                return BookRead.from_orm(db_book)
            return None
        except SQLAlchemyError as e:
            raise e

    async def get_all_books(self, skip: int = 0, limit: int = 10) -> List[BookRead]:
        try:
            result = await self.db.execute(
                select(Book).offset(skip).limit(limit)
            )
            books = result.scalars().all()
            return [BookRead.from_orm(book) for book in books]
        except SQLAlchemyError as e:
            raise e

    async def get_book_by_title(self, title: str) -> Optional[BookRead]:
        try:
            result = await self.db.execute(
                select(Book).where(Book.title == title)
            )
            db_book = result.scalars().first()
            if db_book:
                return BookRead.from_orm(db_book)
            return None
        except SQLAlchemyError as e:
            raise e

    async def update_book(self, book_id: int, book_update: BookUpdate) -> Optional[BookRead]:
        try:
            result = await self.db.execute(
                select(Book).where(Book.id == book_id)
            )
            db_book = result.scalars().first()
            if not db_book:
                return None

            for key, value in book_update.dict(exclude_unset=True).items():
                setattr(db_book, key, value)

            await self.db.commit()
            await self.db.refresh(db_book)
            return BookRead.from_orm(db_book)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e

    async def delete_book(self, book_id: int) -> bool:
        try:
            result = await self.db.execute(
                select(Book).where(Book.id == book_id)
            )
            db_book = result.scalars().first()
            if not db_book:
                return False

            await self.db.delete(db_book)
            await self.db.commit()
            return True
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e