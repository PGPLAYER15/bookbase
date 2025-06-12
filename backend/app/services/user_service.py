from typing import List, Optional
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.repositories.user_repository import RepoUser
from sqlalchemy.exc import SQLAlchemyError
from app.core.security import verify_password

class UserService:
    def __init__(self, user_repo: RepoUser):
        self.user_repo = user_repo

    async def create_user(self, user_data: UserCreate) -> User:
        existing_user = await self.user_repo.get_user_by_email(user_data.email)
        if existing_user:
            raise ValueError("El email ya está registrado")
        return await self.user_repo.create_user(user_data)

    async def get_user(self, user_id: int) -> Optional[User]:
        return await self.user_repo.get_user_by_id(user_id)

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        return await self.user_repo.get_user_by_id(user_id)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        return await self.user_repo.get_user_by_email(email)

    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        return await self.user_repo.update_user(user_id, user_data)

    async def delete_user(self, user_id: int) -> bool:
        return await self.user_repo.delete_user(user_id) 
    
    async def authenticate_user(self, username_or_email: str, password: str):
        user = await self.user_repo.get_user_by_email(username_or_email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user