from typing import Optional, List
from pydantic import EmailStr, BaseModel, Field , field_validator, model_validator
from app.schemas.book import BookRead 

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    user_type: str = Field(default="reader", pattern="^(reader|writer)$")
    
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
    user_type: Optional[str] = Field(default=None, pattern="^(reader|writer)$")

    class Config:
        from_attributes = True

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    liked_books: List[BookRead] = Field(default_factory=list)
    user_type: str

    class Config:
        from_attributes = True

class UserBasicInfo(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True
        
class Token(BaseModel):
    access_token: str
    token_type: str
    user_type: str