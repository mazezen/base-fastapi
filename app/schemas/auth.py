from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from typing_extensions import Annotated

class LoginRequest(BaseModel):
    """Schema for token response."""

    email: EmailStr = Field(..., description="User email")
    password: Annotated[str, Field(..., min_length=8, max_length=128)]

class TokenResponse(BaseModel):
    """Schema for token response."""

    model_config = ConfigDict(from_attributes=True)
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refesh token")
    token_type: str = Field(default="bearer", description="Token type")

class TokenPayload(BaseModel):
    """Schema for token payload."""

    sub: str
    exp: int
    type: str

class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request."""

    resfresh_token: str = Field(..., description="JWT refresh token")

class RegisterRequest(BaseModel):
    """Schema for user registration request."""

    email: EmailStr = Field(..., description="User email")
    username: Annotated[str, Field(..., min_length=3, max_length=150)]
    password: Annotated[str, Field(..., min_length=8, max_length=128)]
    first_name: Annotated[str, Field(default="", max_length=150)]
    last_name: Annotated[str, Field(default="", max_length=150)]

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        """Validate username is alphanumeric."""
        if not v.isalnum():
            raise ValueError("Username must be aplhanumeric")
        return v
    
class RegisterResponse(BaseModel):
    """Schema for user registration response."""

    model_config = ConfigDict(from_attributes=True)
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    is_active: bool
    date_joined: datetime