from typing import List, Optional
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate, BookRead
from app.interfaces.Ibook_repository import BookRepository

class RepoBook(BookRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_book(self, book_data: BookCreate) -> Book:
        try:
            result = await self.db.execute(
                select(Book).where(Book.title == book_data.title)
            )
            if result.scalars().first():
                raise ValueError("El título ya existe")

            book = Book(**book_data.model_dump())
            self.db.add(book)
            await self.db.commit()
            await self.db.refresh(book)
            return book
        except SQLAlchemyError as e:
            await self.db.rollback()
            print(f"Error creando un libro: {e}")
            raise e

    async def get_book_by_id(self, book_id: int) -> Optional[Book]:
        try:
            result = await self.db.execute(select(Book).filter(Book.id == book_id))
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise e

    async def get_all_books(self, skip: int = 0, limit: int = 10) -> List[Book]:
        try:
            result = await self.db.execute(
                select(Book)
                .order_by(Book.created_at.desc())
                .offset(skip)
                .limit(limit)
            )
            return result.scalars().all()
        except Exception as e:
            await self.db.rollback()
            raise e

    async def get_book_by_title(self, title: str) -> Optional[Book]:
        try:
            result = await self.db.execute(select(Book).filter(Book.title == title))
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise e

    async def get_books_by_category(self, category: str, skip: int = 0, limit: int = 10) -> List[Book]:
        try:
            stmt = select(Book).where(Book.category == category).offset(skip).limit(limit)
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            await self.db.rollback()
            raise e

    async def search_books(self, search_term: str, skip: int = 0, limit: int = 10) -> List[Book]:
        try:
            search_pattern = f"%{search_term}%"
            result = await self.db.execute(
                select(Book)
                .filter(
                    or_(
                        Book.title.ilike(search_pattern),
                        Book.author.ilike(search_pattern),
                        Book.description.ilike(search_pattern),
                        Book.category.ilike(search_pattern)
                    )
                )
                .order_by(Book.created_at.desc())
                .offset(skip)
                .limit(limit)
            )
            return result.scalars().all()
        except Exception as e:
            await self.db.rollback()
            raise e

    async def update_book(self, book_id: int, book_data: BookUpdate) -> Optional[Book]:
        try:
            book = await self.get_book_by_id(book_id)
            if not book:
                return None
            
            update_data = book_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(book, key, value)
            
            await self.db.commit()
            await self.db.refresh(book)
            return book
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e

    async def delete_book(self, book_id: int) -> bool:
        try:
            book = await self.get_book_by_id(book_id)
            if not book:
                return False
            
            await self.db.delete(book)
            await self.db.commit()
            return True
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e