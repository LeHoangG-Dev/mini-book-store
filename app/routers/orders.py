from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def create_order():
    pass

@router.get("/")
def list_user_orders():
    pass

@router.get("/{id}")
def get_order_detail(id: int):
    pass

@router.patch("/{id}/cancel")
def cancel_order(id: int):
    pass

@router.get("/admin/all")
def list_all_orders():
    pass

@router.patch("/admin/{id}/status")
def update_order_status(id: int):
    pass