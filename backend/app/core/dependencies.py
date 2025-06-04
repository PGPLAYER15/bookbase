from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import AsyncSessionLocal
from app.services.book_service import BookService
from app.repositories.book_repositor import RepoBook
from app.services.review_service import ReviewService
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.services.user_service import UserService
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

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
    return BookService(RepoBook(db))

def get_review_service(
    review_repo: ReviewRepository = Depends(get_review_repository),
    book_repo: RepoBook = Depends(get_book_repository),
    user_repo: RepoUser = Depends(get_user_repository)
) -> ReviewService:
    return ReviewService(review_repo, book_repo, user_repo)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autenticado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await user_service.get_user_by_id(int(user_id))
    if user is None:
        raise credentials_exception
    return user

from app.models.user import User
from typing import Annotated

DatabaseSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]