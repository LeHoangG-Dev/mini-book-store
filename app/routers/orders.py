from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, require_admin, get_db
from app.schemas.orders import OrderCreate, OrderResponse, OrderStatusUpdate
from app.services.orders import list_orders

router = APIRouter()



@router.get("/admin/all", response_model=list[OrderResponse], status_code=status.HTTP_200_OK)  
def list_all_orders(db: Session = Depends(get_db)):
    return list_orders(db)
    


@router.patch("/admin/{id}/status", response_model=OrderResponse)
def update_order_status():
    pass


@router.get("/", response_model=list[OrderResponse])
def list_user_orders():
    pass


@router.get("/{id}", response_model=OrderResponse)
def get_order_detail():
    pass


@router.patch("/{id}/cancel", response_model=OrderResponse)
def cancel_order():
    pass