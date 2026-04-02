from app.core.base import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100),nullable=False)
    author = Column(String(100),nullable=False)
    price = Column(Float, nullable=False)
  
    order_items = relationship("OrderItem", back_populates = "book")