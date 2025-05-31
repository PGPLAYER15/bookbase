from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ReviewBase(BaseModel):
    comment: Optional[str] = Field(None, max_length=500)
    rating: float = Field(..., ge=1.0, le=5.0)  # Rating entre 1 y 5

class ReviewCreate(ReviewBase):
    user_id: int
    book_id: int

class ReviewUpdate(BaseModel):
    comment: Optional[str] = Field(None, max_length=500)
    rating: Optional[float] = Field(None, ge=1.0, le=5.0)

class ReviewRead(ReviewBase):
    id: int
    user_id: int
    book_id: int
    created_at: datetime

    class Config:
        from_attributes = True