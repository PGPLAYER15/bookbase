from typing import Optional, List
from pydantic import EmailStr, BaseModel, Field
from app.schemas.book import BookRead 

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    liked_books: Optional[List[BookRead]] = Field(default_factory=list)

    class Config:
        from_attributes = True

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    liked_books: List[BookRead] = Field(default_factory=list)

    class Config:
        from_attributes = True