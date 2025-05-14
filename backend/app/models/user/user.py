from sqlalchemy import Column, Integer, String , Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    admin = Column(Boolean, default=False, nullable=False)
    hashed_password = Column(String(128), nullable=False)