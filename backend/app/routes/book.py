from typing import Union
from fastapi import APIRouter,Depends , HTTPException
from sqlalchemy.orm import Session
from app.schemas.book import BookCreate, BookUpdate, BookRead
from app.repositories.book.RepoBook import RepoBook
from app.database import get_db
from app.models.book import Book

router = APIRouter()

@router.post("/books",response_model=BookCreate)
async def create_book(book: BookCreate, db: Session = Depends(get_db)):
    book_repo = RepoBook(db)
    db_book = book_repo.create_book(book)
    return db_book