from fastapi import APIRouter, Depends, HTTPException
from app.core.dependencies import CurrentUser, get_review_service
from app.schemas.review import ReviewRead, ReviewCreate
from typing import List
from app.services.review_service import ReviewService

router = APIRouter(tags=["Reviews"])

@router.post("/books/{book_id}/reviews", response_model=ReviewRead, status_code=201)
async def create_review(
    book_id: int,
    review_data: ReviewCreate,
    current_user: CurrentUser,
    review_service: ReviewService = Depends(get_review_service)
):
    try:
        return review_service.create_review(
            user_id=current_user.id,
            book_id=book_id,
            review_data=review_data
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/books/{book_id}/reviews", response_model=List[ReviewRead])
async def get_book_reviews(
    book_id: int,
    review_service: ReviewService = Depends(get_review_service)
):
    return review_service.get_book_reviews(book_id)