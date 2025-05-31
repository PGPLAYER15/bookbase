from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import AsyncSessionLocal
from app.services.book_service import BookService
from app.services import book_service, review_service, user_service

async def get_db():

    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()

from app.repositories.user_likes_repository import LikeRepository
from app.repositories.user_repository import RepoUser
from app.repositories.review_repository import ReviewRepository
from app.repositories.book_repositor import RepoBook

def get_like_repository(db: Session = Depends(get_db)) -> LikeRepository:
    return LikeRepository(db)

def get_user_repository(db: Session = Depends(get_db)) -> RepoUser:
    return RepoUser(db)

def get_book_repository(db: Session = Depends(get_db)) -> RepoBook:
    return RepoBook(db)

def get_review_repository(db: Session = Depends(get_db)) -> ReviewRepository:
    return ReviewRepository(db)

from app.services.user_likes_service import LikeService
from app.services.user_service import UserService as user_service

def get_like_service(
    like_repo: LikeRepository = Depends(get_like_repository),
    user_repo: RepoUser = Depends(get_user_repository),
    book_repo: RepoBook = Depends(get_book_repository)
) -> LikeService:
    return LikeService(like_repo, user_repo, book_repo)

def get_user_service(
    user_repo: RepoUser = Depends(get_user_repository)
) -> user_service:
    return user_service(user_repo)

def get_book_service(db: Session = Depends(get_db)) -> BookService:
    return book_service(RepoBook(db))

def get_review_service(
    review_repo: ReviewRepository = Depends(get_review_repository),
    book_repo: RepoBook = Depends(get_book_repository),
    user_repo: RepoUser = Depends(get_user_repository)
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

from app.models.user import User

DatabaseSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]