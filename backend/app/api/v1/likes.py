from fastapi import APIRouter, Depends, HTTPException
from backend.app.core.dependencies import CurrentUser, get_like_service
from backend.app.services.user_likes_service import LikeService

router = APIRouter(tags=["Likes"])

@router.post("/books/{book_id}/like", status_code=204)
async def like_book(
    book_id: int,
    current_user: CurrentUser,
    like_service: LikeService = Depends(get_like_service)
):
    if not like_service.add_like(current_user.id, book_id):
        raise HTTPException(status_code=400, detail="El libro ya está en favoritos")

@router.delete("/books/{book_id}/like", status_code=204)
async def unlike_book(
    book_id: int,
    current_user: CurrentUser,
    like_service: LikeService = Depends(get_like_service)
):
    if not like_service.remove_like(current_user.id, book_id):
        raise HTTPException(status_code=404, detail="Like no encontrado")