from pydantic import BaseModel

class UserLikeCreate(BaseModel):
    user_id: int
    book_id: int

class UserLikeRead(BaseModel):
    user_id: int
    book_id: int

    class Config:
        from_attributes = True  