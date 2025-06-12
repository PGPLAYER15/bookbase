from fastapi import APIRouter, Depends, HTTPException, Query
from app.core.dependencies import get_book_service
from app.schemas.book import BookRead, BookCreate, BookUpdate
from app.services.book_service import BookService
from typing import List, Optional
from urllib.parse import unquote

router = APIRouter(tags=["Books"])

@router.post("/books", response_model=BookRead, status_code=201)
async def create_book(
    book_data: BookCreate,
    book_service: BookService = Depends(get_book_service)
):
    try:
        return await book_service.create_book(book_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/books", response_model=List[BookRead])
async def list_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    book_service: BookService = Depends(get_book_service)
):
    if category:
        category = unquote(category)
    
    print(f"Received request - Category: {category}, Search: {search}, Skip: {skip}, Limit: {limit}")
    
    if category:
        print(f"Filtering by category: {category}")
        books = await book_service.get_books_by_category(category, skip, limit)
        print(f"Found {len(books)} books in category {category}")
        return books
    elif search:
        print(f"Searching for: {search}")
        return await book_service.search_books(search, skip, limit)
    
    print("Getting all books")
    return await book_service.get_all_books(skip, limit)

@router.get("/books/{book_id}", response_model=BookRead)
async def get_book(
    book_id: int,
    book_service: BookService = Depends(get_book_service)
):
    book = await book_service.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return book

@router.put("/books/{book_id}", response_model=BookRead)
async def update_book(
    book_id: int,
    book_data: BookUpdate,
    book_service: BookService = Depends(get_book_service)
):
    book = await book_service.update_book(book_id, book_data)
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return book

@router.delete("/books/{book_id}", status_code=204)
async def delete_book(
    book_id: int,
    book_service: BookService = Depends(get_book_service)
):
    success = await book_service.delete_book(book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
