from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.user.user import User
from app.models.book.book import Book

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key= True, index = True)
    comment = Column(Text, nullable=False)
    
    book_id = Column(Integer, ForeignKey("bookm.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    user = relationship("User", back_populates="reviews")
    book = relationship("Book", back_populates="reviews")