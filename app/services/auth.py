from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.jwt import TokenType, create_token, verify_token
from app.exceptions.exception import (
    EmailAlreadyExistError,
    InvalidTokenError,
    TokenExpiredError,
    UserIsInactiveError,
    UsernameAlreadyExistError,
    UsernameOrPasswordIsIncorrectError,
)
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.services.user import UserService

class AuthService:

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.user_service = UserService(db)

    async def register(self, register_data: RegisterRequest) -> User:
        email = str(register_data.email)

        if await self.user_service.get_by_email(email):
            raise EmailAlreadyExistError
        if await self.user_service.get_by_username(register_data.username):
            raise UsernameAlreadyExistError
    
        user = User(
            email=email,
            username = register_data.username,
            first_name = register_data.first_name,
            last_name = register_data.last_name,
            is_active = True,
            date_joined = datetime.now(),
        )
        user.set_password(register_data.password)

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user
    
    async def login(self, login_data: LoginRequest) -> TokenResponse:
        email = str(login_data.email)
        user = await self.user_service.authenticate(
            email=email,
            password=login_data.password,
        )

        if not user:
            raise UsernameOrPasswordIsIncorrectError
        if not user.is_active:
            raise UserIsInactiveError
        
        user.last_login = datetime.now()
        await self.db.commit()

        return TokenResponse(
            access_token = create_token(user.id, TokenType.ACCESS_TOKEN),
            refresh_token = create_token(user.id, TokenType.ACCESS_TOKEN),
        )
    
    async def refresh_token(self, refresh_token: str) -> TokenResponse:
        try: 
            user_id = verify_token(refresh_token, TokenType.ACCESS_TOKEN)
            if not user_id:
                raise InvalidTokenError
            
            user = await self.user_service.get_by_id(user_id=user_id)
            if not user or not user.is_active:
                raise InvalidTokenError
            
            return TokenResponse(
                access_token=create_token(user.id, TokenType.ACCESS_TOKEN),
                refresh_token=create_token(user.id, TokenType.REFRESH_TOKEN),
            )
        
        except TokenExpiredError:
            raise
        except Exception as e:
            raise InvalidTokenError from e
        
    async def logout(self, _user: User) -> dict:
        return {"message": "successfully logged out"}
