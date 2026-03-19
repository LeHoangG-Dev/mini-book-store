from pydantic import BaseModel, Field
from app.schemas.books import BookResponse

#Cart Items
class CartItemBase(BaseModel):
    book_id: int
    quantity: int = Field(gt=0)
    

class CartItemCreate(CartItemBase):
    pass

class CartItemResponse(CartItemBase):
    id: int
    user_id: int
    book: BookResponse

    model_config = {"from_attributes": True}

class CartItemUpdate(BaseModel):
    quantity: int = Field(gt=0)




