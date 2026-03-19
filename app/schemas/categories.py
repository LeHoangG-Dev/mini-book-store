from pydantic import BaseModel, Field
from datetime import datetime

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=20)
    description: str | None = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    is_active: bool
    created_at: datetime
    update_at: datetime | None = None

    model_config = {"from_attributes": True}

class CategoryUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=20)
    description: str | None = None
    is_active: bool | None = None   
    
