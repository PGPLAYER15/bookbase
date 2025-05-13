from pydantic import BaseModel, EmailStr
from typing import List

class UserBase(BaseModel):
    username: str
    email: EmailStr
    favoritos: List[int] = []

class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True