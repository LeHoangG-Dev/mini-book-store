from sqlalchemy import Column, Integer, Numeric, String, Text, DateTime, ForeignKey, Enum as SAEnum
from app.core.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import func
import enum



class OrderStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    shipping = "shipping"
    delivered = "delivered"
    cancelled = "cancelled"
    shipped = "shipped"



class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete= "SET NULL"), nullable=True)
    status          = Column(SAEnum(OrderStatus), default=OrderStatus.pending, nullable=False)
    total_price     = Column(Numeric(14, 2), nullable=False)
    shipping_address = Column(Text, nullable=False)
    phone           = Column(String(20), nullable=False)
    note            = Column(Text, nullable=True)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())
    updated_at      = Column(DateTime(timezone=True), onupdate=func.now())

    user  = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id          = Column(Integer, primary_key=True, index=True)
    order_id    = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    book_id     = Column(Integer, ForeignKey("books.id", ondelete="SET NULL"), nullable=True)
    quantity    = Column(Integer, nullable=False)
    unit_price  = Column(Numeric(12, 2), nullable=False)  # snapshot giá lúc đặt hàng

    order = relationship("Order", back_populates="items")
    book  = relationship("Book", back_populates="order_items")