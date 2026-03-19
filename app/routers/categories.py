from fastapi import APIRouter, status, Depends, HTTPException
from app.schemas.categories import CategoryCreate, CategoryResponse, CategoryUpdate
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.services.categories import add_category, list_categories, update_categories, remove_category
from typing import List


router = APIRouter()
@router.get("/", response_model= List[CategoryResponse], status_code=status.HTTP_200_OK)
def get_categories(db: Session = Depends(get_db)):
    return list_categories(db)


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return add_category(db, category)


@router.put("/{id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def put_category(category_update: CategoryUpdate,id: int, db: Session = Depends(get_db)):
    return update_categories(db, id, category_update)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: int, db: Session = Depends(get_db)):
    db_category = remove_category(db, id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")