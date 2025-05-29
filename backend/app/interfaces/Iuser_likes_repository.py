from abc import ABC, abstractmethod
from typing import List, Optional

class ILikeRepository(ABC):
    @abstractmethod
    def add_like(self, user_id: int, book_id: int) -> bool:
        pass

    @abstractmethod
    def remove_like(self, user_id: int, book_id: int) -> bool:
        pass

    @abstractmethod
    def get_user_likes(self, user_id: int) -> List[int]:
        pass

    @abstractmethod
    def count_likes_for_book(self, book_id: int) -> int:
        pass