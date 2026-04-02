# schemas/order.py
from pydantic import BaseModel, Field, model_validator
from decimal import Decimal
from datetime import datetime
from typing import Optional
from app.models.orders import OrderStatus


# ── OrderItem ──────────────────────────────────────────
class OrderItemBase(BaseModel):
    book_id: int = Field(..., example=1)
    quantity: int = Field(..., gt=0, example=2)


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    id: int
    unit_price: Decimal = Field(..., example=150000)

    class Config:
        from_attributes = True


# ── Order ──────────────────────────────────────────────
class OrderBase(BaseModel):
    shipping_address: str = Field(..., min_length=5, max_length=500, example="123 Nguyễn Huệ, Q1, HCM")
    phone: str = Field(..., min_length=9, max_length=15, example="0909123456")
    note: Optional[str] = Field(None, max_length=500, example="Giao giờ hành chính")


class OrderCreate(OrderBase):
    items: list[OrderItemCreate] = Field(..., min_length=1)

    @model_validator(mode="after")
    def items_not_empty(self):
        if not self.items:
            raise ValueError("Order phải có ít nhất 1 sản phẩm")
        return self


class OrderStatusUpdate(BaseModel):
    status: OrderStatus = Field(..., example=OrderStatus.confirmed)


class OrderResponse(OrderBase):
    id: int
    user_id: Optional[int]
    status: OrderStatus
    total_price: Decimal = Field(..., example=300000)
    items: list[OrderItemResponse]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True