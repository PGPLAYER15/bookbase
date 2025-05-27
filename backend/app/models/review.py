from sqlalchemy import Column, Integer, Text,DateTime, Float,ForeignKey
from datetime import datetime 
from sqlalchemy.orm import relationship
from app.database import Base
from backend.app.models.user import User
from backend.app.models.book import Book

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key= True, index = True)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    rating = Column(Float, nullable=True)
    
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    user = relationship("User", back_populates="reviews")
    book = relationship("Book", back_populates="reviews",cascade="all, delete")   
