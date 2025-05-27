from typing import Optional, List
from pydantic import EmailStr, BaseModel, Field , field_validator, model_validator
from app.schemas.book import BookRead 

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    
    @field_validator('username')
    def name_must_contian_text(cls, v):
        if len(v) < 3 or len(v) > 50:
            raise ValueError('username must be between 3 and 50 characters')
        return v

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

class UserBasicInfo(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True