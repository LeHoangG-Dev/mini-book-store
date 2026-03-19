from app.core.base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    book_id = Column(Integer,ForeignKey("books.id"))
    quantity = Column(Integer, nullable=False, default=1)

    book = relationship("Book")

    __table_args__ = (
        UniqueConstraint("user_id", "book_id"),
    )

