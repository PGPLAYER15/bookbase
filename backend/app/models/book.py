from sqlalchemy import Column, Integer, String ,Text,ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from backend.app.models.user_likes import user_likes



class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    link = Column(Text, unique=True, index=True, nullable=True)
    description = Column(Text, nullable=True)
    
    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")

    liked_by_users = relationship(
        "User",
        secondary=user_likes,
        back_populates="liked_books"
    )