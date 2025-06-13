from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserRead
from app.interfaces.Iuser_repository import UserRepository
from app.core.security import get_password_hash

class RepoUser(UserRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user: UserCreate) -> User:
        try:
            result = await self.db.execute(select(User).where(User.email == user.email))
            if result.scalars().first():
                raise ValueError("El email ya está registrado")
            
            hashed_password = get_password_hash(user.password)
            db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            user_type=user.user_type
            )
            self.db.add(db_user)
            await self.db.commit()
            await self.db.refresh(db_user)
            return db_user
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        try:
            result = await self.db.execute(select(User).where(User.id == user_id))
            return result.scalars().first()
        except SQLAlchemyError as e:
            raise e

    async def get_user_by_email(self, email: str) -> Optional[User]:
        try:
            result = await self.db.execute(select(User).where(User.email == email))
            return result.scalars().first()
        except SQLAlchemyError as e:
            raise e

    async def get_users(self) -> List[User]:
        try:
            result = await self.db.execute(select(User))
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise e

    async def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        try:
            result = await self.db.execute(select(User).where(User.id == user_id))
            db_user = result.scalars().first()
            if not db_user:
                return None

            for key, value in user_update.dict(exclude_unset=True).items():
                setattr(db_user, key, value)

            await self.db.commit()
            await self.db.refresh(db_user)
            return db_user
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e

    async def delete_user(self, user_id: int) -> bool:
        try:
            result = await self.db.execute(select(User).where(User.id == user_id))
            db_user = result.scalars().first()
            if not db_user:
                return False

            await self.db.delete(db_user)
            await self.db.commit()
            return True
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e