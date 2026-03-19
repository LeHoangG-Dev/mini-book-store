from pydantic import BaseModel, EmailStr, field_validator, Field
from datetime import datetime

#Token Schemas
class TokenBase(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class Token(TokenBase):
    pass

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class RefreshTokenResponse(TokenBase):
    pass

class RevokeTokenRequest(BaseModel):
    refresh_token: str

#Auth Request Schemas

class AuthBase(BaseModel):
    email: EmailStr

class LoginRequest(AuthBase):
    password: str

class RegisterRequest(AuthBase):
    username: str = Field(..., min_length=3, max_length=50)
    password: str
    full_name: str | None = None

    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

# Auth Response Schemas
class AuthResponseBase(TokenBase):
    user_id: int
    email: EmailStr

class LoginResponse(AuthResponseBase):
    pass

class RegisterResponse(AuthResponseBase):
    message: str = "Registration successful"

#RefreshToken DB Schemas
class RefreshTokenBase(BaseModel):
    token: str
    expires_at: datetime

class RefreshTokenCreate(RefreshTokenBase):
    user_id: int

class RefreshTokenResponse(RefreshTokenBase):
    id: int 
    user_id: int
    is_revoked: bool
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True

#JWT Payload
class TokenPayLoad(BaseModel):
    sub: int
    exp: datetime
    iat: datetime

