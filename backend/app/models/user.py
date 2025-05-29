from sqlalchemy import Column, Integer, String , Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.user_likes import user_likes

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    admin = Column(Boolean, default=False, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    
    liked_books = relationship(
        "Book",
        secondary=user_likes,
        back_populates="liked_by_users",
        lazy="selectin"
    )