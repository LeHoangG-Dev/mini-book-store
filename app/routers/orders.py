from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db, require_user, require_admin
from app.models.users import User
from app.schemas.orders import CheckoutRequest, OrderResponse
from app.services.orders import (
    checkout, get_orders, get_order,
    admin_confirm, admin_ship, admin_shipped, admin_cancel,
    user_cancel, user_received,
)

router = APIRouter()

@router.post("/checkout", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def post_checkout(
    payload: CheckoutRequest,
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    """Chuyển toàn bộ cart của user thành một order mới."""
    return checkout(db, current_user.id, payload)


@router.get("/", response_model=List[OrderResponse])
def get_my_orders(
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    """Lịch sử đơn hàng của user."""
    return get_orders(db, current_user.id)


@router.get("/{order_id}", response_model=OrderResponse)
def get_my_order(
    order_id: int,
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    """Chi tiết một đơn hàng."""
    return get_order(db, current_user.id, order_id)


@router.patch("/{order_id}/cancel", response_model=OrderResponse)
def cancel_my_order(
    order_id: int,
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    return user_cancel(db, current_user.id, order_id)


@router.patch("/{order_id}/received", response_model=OrderResponse)
def confirm_received(
    order_id: int,
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    return user_received(db, current_user.id, order_id)


# ── Admin routes ───────────────────────────────────────────────────────────────

@router.patch("/admin/{order_id}/confirm", response_model=OrderResponse)
def admin_confirm_order(
    order_id: int,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return admin_confirm(db, order_id)


@router.patch("/admin/{order_id}/ship", response_model=OrderResponse)
def admin_ship_order(
    order_id: int,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return admin_ship(db, order_id)


@router.patch("/admin/{order_id}/shipped", response_model=OrderResponse)
def admin_shipped_order(
    order_id: int,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return admin_shipped(db, order_id)


@router.patch("/admin/{order_id}/cancel", response_model=OrderResponse)
def admin_cancel_order(
    order_id: int,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return admin_cancel(db, order_id)