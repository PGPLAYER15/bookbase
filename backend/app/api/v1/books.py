from fastapi import APIRouter, Depends, HTTPException
from backend.app.core.dependencies import get_book_service
from app.schemas.book import BookRead, BookCreate, BookUpdate
from backend.app.services.book_service import BookService
from typing import List

router = APIRouter(tags=["Books"])

@router.post("/books", response_model=BookRead, status_code=201)
async def create_book(
    book_data: BookCreate,
    book_service: BookService = Depends(get_book_service)
):
    try:
        return book_service.create_book(book_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/books", response_model=List[BookRead])
async def list_books(
    skip: int = 0,
    limit: int = 10,
    book_service: BookService = Depends(get_book_service)
):
    return book_service.get_all_books(skip=skip, limit=limit)