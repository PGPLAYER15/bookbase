from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    name: str
    link: str
    description: Optional[str] = None

class BookRead(BaseModel):
    id: int
    name: str
    link: str

    class Config:
        from_attributes = True

class BookUpdate(BaseModel):
    name: Optional[str] = None
    link: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True