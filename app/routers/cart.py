from fastapi import APIRouter, status, Depends, HTTPException
from app.services.cart import add_item, list_item, update_item, remove_item
from app.schemas.cart import CartItemResponse, CartItemUpdate, CartItemCreate
from app.core.dependencies import get_current_user, get_db, require_user
from sqlalchemy.orm import Session
from app.models.users import User
from typing import List

router = APIRouter()

#hard id
id: int = 1
#########

@router.get("/", response_model=List[CartItemResponse])
def get_cart(_ :User = Depends(require_user),db: Session = Depends(get_db)):
    return list_item(db)
    


@router.post("/items", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
def post_item(item_create: CartItemCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return add_item(db, current_user.id, item_create)


@router.put("/items/{book_id}", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
def put_item(item_update: CartItemUpdate, book_id: int, _ :User = Depends(require_user),db: Session = Depends(get_db)):
    return update_item(db, book_id, item_update)


@router.delete("/items/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(book_id: int,_ :User = Depends(require_user), db: Session = Depends(get_db)):
    db_item = remove_item(db, book_id)
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")



