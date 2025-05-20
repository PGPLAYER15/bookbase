from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.user.user import User
from app.schemas.user import UserCreate, UserUpdate, UserRead
from app.repositories.user.IRepoUser import UserRepository

class RepoUser(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate) -> User:
        db_user = User(**user.dict())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_user_by_id(self, user_id: int) -> Optional[UserRead]:
        return self.db.query(User).filter(User.id == user_id).first()
    def get_user_by_email(self, email: str) -> Optional[UserRead]:
        return self.db.query(User).filter(User.email == email).first()

    def get_users(self, skip: int = 0, limit: int = 100) -> List[UserRead]:
        return self.db.query(User).offset(skip).limit(limit).all()

    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[UserRead]:
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return None
        for key, value in user_update.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int) -> bool:
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return False
        self.db.delete(db_user)
        self.db.commit()
        return True 