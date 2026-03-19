from sqlalchemy.orm import Session
from app.schemas.categories import CategoryCreate, CategoryUpdate
from app.models.categories import Category

def add_category(db: Session, category: CategoryCreate):
    db_category = Category(
        name=category.name,
        description=category.description
    )

    db.add(db_category)
    try:
        db.commit()
        db.refresh(db_category)
    except Exception as e:
        db.rollback()
        raise e
    
    return db_category

def list_categories(db: Session):
    return db.query(Category).all()

def update_categories(db: Session, category_id: int, category_update: CategoryUpdate):
    db_category = db.query(Category).filter(Category.id == category_id).first()

    if not db_category:
        return None
    
    for key, value in category_update.model_dump(exclude_unset=True).items():
        setattr(db_category, key, value)

    try:
        db.commit()
        db.refresh(db_category)
    except Exception as e:
        db.rollback()
        raise e
    
    return db_category

def remove_category(db: Session, category_id):
    db_category = db.query(Category).filter(Category.id == category_id).first()

    if not db_category:
        return None
    
    db.delete(db_category)
    
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    
    return db_category
