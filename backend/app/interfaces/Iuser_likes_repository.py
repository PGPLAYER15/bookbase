from abc import ABC, abstractmethod
from typing import List, Optional

class ILikeRepository(ABC):
    @abstractmethod
    def add_like(self, user_id: int, book_id: int) -> bool:
        """Añade un like. Devuelve True si fue exitoso, False si ya existía."""
        pass

    @abstractmethod
    def remove_like(self, user_id: int, book_id: int) -> bool:
        """Elimina un like. Devuelve True si fue exitoso, False si no existía."""
        pass

    @abstractmethod
    def get_user_likes(self, user_id: int) -> List[int]:
        """Devuelve los IDs de los libros que el usuario ha dado like."""
        pass

    @abstractmethod
    def count_likes_for_book(self, book_id: int) -> int:
        """Cuenta cuántos likes tiene un libro."""
        pass