from sqlalchemy import Column, Integer, String ,Text,ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.user.user_likes import user_likes



class Book(Base):
    __tablename__ = "bookm"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    link = Column(String(120), unique=True, index=True, nullable=False)
    
    reviews = relationship("Review", back_populates="book" ,cascade="all, delete-orphan")

    liked_by_users = relationship(
        "User",
        secondary=user_likes,
        back_populates="liked_books"
    )