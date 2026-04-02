# schemas/order.py
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import Optional, List
from app.models.orders import OrderStatus



class CheckoutRequest(BaseModel):
    shipping_address: str
    phone: str
    note: Optional[str] = None

class OrderItemResponse(BaseModel):
    id: int
    book_id: Optional[int]
    quantity: int
    unit_price: Decimal

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    status: OrderStatus
    total_price: Decimal
    shipping_address: str
    phone: str
    note: Optional[str]
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True