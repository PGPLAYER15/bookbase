from fastapi import APIRouter, Depends, HTTPException
from app.core.dependencies import CurrentUser, get_user_service
from app.schemas.user import UserRead, UserUpdate
from app.services.user_service import UserService

router = APIRouter(tags=["Users"])

@router.get("/users/me", response_model=UserRead)
async def read_current_user(current_user: CurrentUser):
    return current_user

@router.patch("/users/me", response_model=UserRead)
async def update_current_user(
    user_data: UserUpdate,
    current_user: CurrentUser,
    user_service: UserService = Depends(get_user_service)
):
    try:
        return await user_service.update_user(current_user.id, user_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))