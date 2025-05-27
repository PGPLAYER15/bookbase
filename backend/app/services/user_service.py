from typing import List, Optional
from app.models import User
from app.schemas import UserCreate, UserUpdate
from app.repositories import UserRepository
from sqlalchemy.exc import SQLAlchemyError

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, user_data: UserCreate) -> User:
        existing_user = self.user_repo.get_user_by_email(user_data.email)
        if existing_user:
            raise ValueError("El email ya está registrado")
        return self.user_repo.create_user(user_data)

    def get_user(self, user_id: int) -> Optional[User]:
        return self.user_repo.get_user_by_id(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.user_repo.get_user_by_email(email)

    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        return self.user_repo.update_user(user_id, user_data)

    def delete_user(self, user_id: int) -> bool:
        return self.user_repo.delete_user(user_id)