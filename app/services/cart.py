from sqlalchemy.orm import Session
from app.schemas.cart import CartItemCreate, CartItemUpdate
from app.models.cart import CartItem


def add_item(db: Session, user_id: int, item_created: CartItemCreate):
    db_item = db.query(CartItem).filter(
        CartItem.user_id == user_id,
        CartItem.book_id == item_created.book_id
    ).first()

    if db_item:
        db_item.quantity += item_created.quantity
    else:
        db_item = CartItem(
            user_id=user_id,
            book_id=item_created.book_id,
            quantity=item_created.quantity
        )
        db.add(db_item)

    try:
        db.commit()
        db.refresh(db_item)
    except Exception as e:
        db.rollback()
        raise e
    
    return db_item

def list_item(db: Session):
    return db.query(CartItem).all()

def update_item(db: Session, item_id: int, item_update: CartItemUpdate):
    db_cart_item = db.query(CartItem).filter(CartItem.id == item_id).first()

    if not db_cart_item:
        return None
    
    update_data = item_update.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_cart_item, key, value)

    try:
        db.commit()
        db.refresh(db_cart_item)
    except Exception as e:
        db.rollback()
        raise e

    return db_cart_item

def remove_item(db: Session, item_id: int):
    db_item = db.query(CartItem).filter(CartItem.id == item_id).first()

    if not db_item:
        return None
    
    try:
        db.delete(db_item)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    
    return db_item