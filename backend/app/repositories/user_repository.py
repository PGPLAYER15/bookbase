from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from backend.app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserRead
from backend.app.interfaces.Iuser_repository import UserRepository

class RepoUser(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate) -> User:
        try:
            if self.db.query(User).filter(User.email == user.email).first():
                raise ValueError("El email ya está registrado")

            db_user = User(**user.dict())
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        try:
            return self.db.query(User).filter(User.id == user_id).first()
        except SQLAlchemyError as e:
            raise e

    def get_user_by_email(self, email: str) -> Optional[User]:
        try:
            return self.db.query(User).filter(User.email == email).first()
        except SQLAlchemyError as e:
            raise e

    def get_users(self) -> List[User]:
        try:
            return self.db.query(User).all()
        except SQLAlchemyError as e:
            raise e

    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        try:
            db_user = self.db.query(User).filter(User.id == user_id).first()
            if not db_user:
                return None

            for key, value in user_update.dict(exclude_unset=True).items():
                setattr(db_user, key, value)
            
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def delete_user(self, user_id: int) -> bool:
        try:
            db_user = self.db.query(User).filter(User.id == user_id).first()
            if not db_user:
                return False

            self.db.delete(db_user)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e