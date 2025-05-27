from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from backend.app.services import book_service, review_service, user_service

def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from app.repositories import (
    LikeRepository,
    UserRepository,
    BookRepository,
    ReviewRepository
)

def get_like_repository(db: Session = Depends(get_db)) -> LikeRepository:
    return LikeRepository(db)

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_book_repository(db: Session = Depends(get_db)) -> BookRepository:
    return BookRepository(db)

def get_review_repository(db: Session = Depends(get_db)) -> ReviewRepository:
    return ReviewRepository(db)

from app.services import (
    LikeService
)

def get_like_service(
    like_repo: LikeRepository = Depends(get_like_repository),
    user_repo: UserRepository = Depends(get_user_repository),
    book_repo: BookRepository = Depends(get_book_repository)
) -> LikeService:
    return LikeService(like_repo, user_repo, book_repo)

def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository)
) -> user_service:
    return user_service(user_repo)

def get_book_service(
    book_repo: BookRepository = Depends(get_book_repository)
) -> book_service:
    return book_service(book_repo)

def get_review_service(
    review_repo: ReviewRepository = Depends(get_review_repository),
    book_repo: BookRepository = Depends(get_book_repository),
    user_repo: UserRepository = Depends(get_user_repository)
) -> review_service:
    return review_service(review_repo, book_repo, user_repo)


from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: user_service = Depends(get_user_service)
):

    pass

from backend.app.models.user import User

DatabaseSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]