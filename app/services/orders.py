from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.orders import Order, OrderItem, OrderStatus
from app.models.cart import CartItem       
from app.schemas.orders import CheckoutRequest
from decimal import Decimal

def checkout(db: Session, user_id: int, payload: CheckoutRequest) -> Order:
    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    if not cart_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty"
        )
    
    total: Decimal = sum(
        item.book.price * item.quantity for item in cart_items
    )

    order = Order(
        user_id=user_id,
        total_price=total,
        shipping_address=payload.shipping_address,
        phone=payload.phone,
        note=payload.note,
    )
    db.add(order)
    db.flush()  # để lấy order.id trước khi commit

    # 4. Snapshot từng item vào OrderItem
    for item in cart_items:
        db.add(OrderItem(
            order_id=order.id,
            book_id=item.book_id,
            quantity=item.quantity,
            unit_price=item.book.price,   # snapshot giá tại thời điểm đặt
        ))

    # 5. Clear cart
    for item in cart_items:
        db.delete(item)

    db.commit()
    db.refresh(order)
    return order


def get_orders(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()


def get_order(db: Session, user_id: int, order_id: int) -> Order:
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == user_id
    ).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order

#admin
def _get_order_or_404(db: Session, order_id: int) -> Order:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order

def admin_confirm(db: Session, order_id: int) -> Order:
    order = _get_order_or_404(db, order_id)
    if order.status != OrderStatus.pending:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot confirm order with status '{order.status}'"
        )
    order.status = OrderStatus.confirmed
    db.commit()
    db.refresh(order)
    return order


def admin_ship(db: Session, order_id: int) -> Order:
    order = _get_order_or_404(db, order_id)
    if order.status != OrderStatus.confirmed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot ship order with status '{order.status}'"
        )
    order.status = OrderStatus.shipping
    db.commit()
    db.refresh(order)
    return order


def admin_shipped(db: Session, order_id: int) -> Order:
    order = _get_order_or_404(db, order_id)
    if order.status != OrderStatus.shipping:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot mark shipped with status '{order.status}'"
        )
    order.status = OrderStatus.shipped
    db.commit()
    db.refresh(order)
    return order


def admin_cancel(db: Session, order_id: int) -> Order:
    order = _get_order_or_404(db, order_id)
    if order.status in [OrderStatus.shipped, OrderStatus.delivered]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot cancel order that has already been shipped or delivered"
        )
    order.status = OrderStatus.cancelled
    db.commit()
    db.refresh(order)
    return order

#User
def user_cancel(db: Session, user_id: int, order_id: int) -> Order:
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == user_id
    ).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    if order.status != OrderStatus.pending:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can only cancel orders that are still pending"
        )
    order.status = OrderStatus.cancelled
    db.commit()
    db.refresh(order)
    return order


def user_received(db: Session, user_id: int, order_id: int) -> Order:
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == user_id
    ).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    if order.status != OrderStatus.shipped:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can only confirm receipt when order has been shipped"
        )
    order.status = OrderStatus.delivered
    db.commit()
    db.refresh(order)
    return order