from typing import Union
from fastapi import FastAPI ,APIRouter,Depends , HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdate, UserRead
from app.repositories.RepoUser import RepoUser
from app.dependencies import get_db

router = APIRouter()

@router.post("/users", response_model=UserRead)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_repo = RepoUser(db)
    db_user = user_repo.create_user(user)
    return db_user

@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    repo = RepoUser(db)
    user = repo.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user