from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database import Base

user_likes = Table(
    "user_likes",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("book_id", Integer, ForeignKey("books.id"), primary_key=True)
)