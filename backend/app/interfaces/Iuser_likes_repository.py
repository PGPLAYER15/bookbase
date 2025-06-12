from abc import ABC, abstractmethod
from typing import List, Optional

class ILikeRepository(ABC):
    @abstractmethod
    async def add_like(self, user_id: int, book_id: int) -> bool:
        pass

    @abstractmethod
    async def remove_like(self, user_id: int, book_id: int) -> bool:
        pass

    @abstractmethod
    async def get_user_likes(self, user_id: int) -> List[int]:
        pass

    @abstractmethod
    async def count_likes_for_book(self, book_id: int) -> int:
        pass