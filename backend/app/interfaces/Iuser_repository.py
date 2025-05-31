from abc import ABC, abstractmethod
from typing import  Optional
from app.schemas.user import UserCreate, UserUpdate, UserRead

class UserRepository(ABC):
    @abstractmethod
    def create_user(self, user: UserCreate) -> UserRead:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[UserRead]:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[UserRead]:
        pass

    @abstractmethod
    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[UserRead]:
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> bool:
        pass
