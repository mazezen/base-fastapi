from typing import Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_active_user, get_current_active_superuser, get_db
from app.exceptions.exception import UserNotFoundError
from app.models.user import User
from app.schemas.common import PaginationParams
from app.schemas.user import User as UserSchema
from app.schemas.user import UserCreate, UserUpdate
from app.services.user import UserService

router = APIRouter()

@router.post(
    "",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create user user",
    description="Create user user with email and username. "
    "Only superuser can create new users.",
)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_active_superuser),
) -> UserSchema:
    user_service = UserService(db)
    return await user_service.create(user_in)

@router.get(
    "/me",
    response_model=UserSchema,
    summary="Get current user info",
    description="Get infomation about currently logged in user.",
)
async def read_user_me(
    current_user: User = Depends(get_current_active_user),
) -> UserSchema:
    return current_user


@router.patch(
    "/me",
    response_model=UserSchema,
    summary="Update current user",
    description="Update information for currently logged in user.",
)
async def update_user_me(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> UserSchema:
    user_service = UserService(db)
    return await user_service.update(current_user.id, user_in)

@router.get(
    "/{user_id}",
    response_model=UserSchema,
    summary="Get user by id",
    description="Get user information by id. "
    "Only superuser can access other users' info.",
)
async def read_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_active_superuser),
) -> UserSchema:
    
    user_service = UserService(db)
    user = await user_service.get_by_id(user_id)
    if not user:
        raise UserNotFoundError
    return user