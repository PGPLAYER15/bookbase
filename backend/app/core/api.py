from fastapi import APIRouter
from app.api.v1 import (
    users
)
from app.api.v1 import books, likes, review
from app.api import auth

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(books.router)
api_router.include_router(review.router)
api_router.include_router(likes.router)