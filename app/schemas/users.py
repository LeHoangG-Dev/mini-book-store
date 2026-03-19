from pydantic import BaseModel, Field, EmailStr, field_validator
from app.models.users import UserRole
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str | None = Field(None, max_length=255)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=12)

class UserUpdate(UserBase):
    email: EmailStr | None = None
    username: str | None = Field(None, min_length=3, max_length=50)
    full_name: str | None = Field(None, max_length=255)

class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime | None 

    class Config:
        from_attributes = True

class ChangePasswordRequest(BaseModel):
    old_password: str = Field(..., min_length=6, max_length=12)
    new_password: str = Field(..., min_length=6, max_length=12)

    @field_validator("new_password") #test @classmethod
    def passwords_different(cls, v, values):
        if values.data.get("old_password") and v == values.data.get("old_password"):
            raise ValueError("New password must be different from old password")
        return v
    
class MessageResponse(BaseModel):
    message: str