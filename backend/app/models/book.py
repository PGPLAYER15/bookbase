from sqlalchemy import Column, Integer, String ,Text,ForeignKey,DateTime,func
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.user_likes import user_likes


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), unique=True, index=True, nullable=False)
    link = Column(Text, unique=True, index=True, nullable=True)
    description = Column(Text, nullable=True)
    author = Column(String(255), nullable=False)
    category = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")

    liked_by_users = relationship(
        "User",
        secondary=user_likes,
        back_populates="liked_books"
    )