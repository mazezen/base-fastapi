from typing import AsyncGenerator
from datetime import UTC, datetime, timedelta
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.jwt import verify_token
from app.db.session import AsyncSessionLocal
from app.exceptions.exception import (
    NotSuperuserError,
    UserIsInactiveError,
    UserNotFoundError,
)
from app.models.user import User
from app.services.user import UserService

credentials = HTTPBearer()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session."""
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def get_current_user(
    session: AsyncSession = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(credentials),
) -> User:
    """Get current user from token."""

    user_id = verify_token(token=token.credentials, token_type="access")
    user_service = UserService(session)
    user = await user_service.get_by_id(user_id)
    if not user:
        raise UserNotFoundError
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise UserIsInactiveError
    return current_user

async def get_current_active_superuser(
    current_user: User = Depends(get_current_active_user),
) -> User:
    if not current_user.is_superuser:
        raise NotSuperuserError
    return current_user

