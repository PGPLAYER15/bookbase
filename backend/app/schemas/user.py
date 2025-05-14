from typing import Optional, List
from pydantic import EmailStr , BaseModel, Field


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    favoritos: List[int] = Field(default_factory=list)

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    favoritos: Optional[List[int]] = Field(default=None)
    password: Optional[str] = None

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    favoritos: List[int] = Field(default_factory=list)
    
    class Config:
        from_attributes = True
