from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from app.models.user_likes import user_likes
from app.interfaces.Iuser_likes_repository import ILikeRepository

class LikeRepository(ILikeRepository):
    def __init__(self, db: Session):
        self.db = db

    def add_like(self, user_id: int, book_id: int) -> bool:
        try:
            if self.db.execute(
                user_likes.select().where(
                    user_likes.c.user_id == user_id,
                    user_likes.c.book_id == book_id
                )
            ).fetchone():
                return False

            self.db.execute(
                user_likes.insert().values(user_id=user_id, book_id=book_id)
            )
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e 

    def remove_like(self, user_id: int, book_id: int) -> bool:
        try:
            result = self.db.execute(
                user_likes.delete().where(
                    user_likes.c.user_id == user_id,
                    user_likes.c.book_id == book_id
                )
            )
            self.db.commit()
            return result.rowcount > 0
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def get_user_likes(self, user_id: int) -> List[int]:
        try:
            result = self.db.execute(
                user_likes.select().where(user_likes.c.user_id == user_id)
            )
            return [row.book_id for row in result]
        except SQLAlchemyError as e:
            raise e

    def count_likes_for_book(self, book_id: int) -> int:
        try:
            result = self.db.execute(
                user_likes.select().where(user_likes.c.book_id == book_id)
            )
            return len(result.fetchall())
        except SQLAlchemyError as e:
            raise e