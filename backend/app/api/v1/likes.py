from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import get_current_user, get_like_service
from app.services.user_likes_service import LikeService
from typing import List

router = APIRouter()

@router.post("/books/{book_id}/like", status_code=204)
async def like_book(
    book_id: int,
    current_user = Depends(get_current_user),
    like_service: LikeService = Depends(get_like_service)
):
    try:
        await like_service.add_like(current_user.id, book_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/books/{book_id}/like", status_code=204)
async def unlike_book(
    book_id: int,
    current_user = Depends(get_current_user),
    like_service: LikeService = Depends(get_like_service)
):
    try:
        await like_service.remove_like(current_user.id, book_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/users/me/likes", response_model=List[int])
async def get_user_likes(
    current_user = Depends(get_current_user),
    like_service: LikeService = Depends(get_like_service)
):
    return await like_service.get_user_likes(current_user.id)

@router.get("/books/{book_id}/likes/count")
async def count_book_likes(
    book_id: int,
    like_service: LikeService = Depends(get_like_service)
):
    return {"count": await like_service.count_likes_for_book(book_id)}