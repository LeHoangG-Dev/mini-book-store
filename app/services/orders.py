from sqlalchemy.orm import Session
from app.models.orders import Order, OrderItem
from app.schemas.orders import OrderCreate, OrderItemCreate

def list_orders(db: Session):
    return db.query(Order).all()