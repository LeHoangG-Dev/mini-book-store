import enum
from app.core.base import Base
from sqlalchemy import Column, Integer, Boolean, String, Enum as SAEnum, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class UserRole(str, enum.Enum):
    admin = "admin"
    customer = "customer"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100),unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name= Column(String(255), nullable=True)
    role = Column(SAEnum(UserRole), default=UserRole.customer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    #cart = relationship("cart", back_populates="user", uselist=False)
    orders         = relationship("Order",        back_populates="user")
    # reviews        = relationship("Review",       back_populates="user")