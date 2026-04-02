from fastapi import APIRouter, status, HTTPException, Depends
from ..schemas.books import BookCreate, BookUpdate, BookResponse
from typing import List
from app.core.dependencies import get_db
from app.services.books import get_all_books, get_book_by_id, add_book, update_book, delete_book
from sqlalchemy.orm import Session
from app.models.users import User
from app.core.dependencies import require_admin, require_user

router = APIRouter()


@router.get("/", response_model= List[BookResponse], status_code=status.HTTP_200_OK)
def get_books(db: Session = Depends(get_db)):
    return get_all_books(db)

@router.get("/{id}", response_model=BookResponse, status_code = status.HTTP_200_OK)
def get_book(id: int, db: Session = Depends(get_db)):
    book = get_book_by_id(db, id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with {id} not found") 
    return book

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, _:User = Depends(require_admin),db: Session = Depends(get_db)):
    return add_book(db, book)

@router.put("/{id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
def updated_book(id: int, book: BookUpdate, _:User = Depends(require_admin),db: Session = Depends(get_db)):
    db_book = update_book(db, id, book)
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with {id} not found")
    return db_book


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleted_book(id: int, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    db_book = delete_book(db,id)
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book not found")
   
#Query Params
#search=&category=&min_price=&max_price=&sort_by=price&order=asc&page=1&limit=10
