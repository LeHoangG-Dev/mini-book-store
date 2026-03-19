from app.models.books import Book
from app.schemas.books import BookCreate, BookUpdate
from sqlalchemy.orm import Session

def get_all_books(db: Session):
    return db.query(Book).all()

def get_book_by_id(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

def add_book(db: Session, book: BookCreate):
    db_book = Book(
        title=book.title,
        author=book.author,
        price=book.price
    )
    db.add(db_book)
    try:
        db.commit()
        db.refresh(db_book)
    except Exception as e:
        db.rollback()
        raise  e
    
    return db_book

def update_book(db: Session, book_id: int, book: BookUpdate):
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        return None
    
    update_data = book.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)
    
    try:
        db.commit()
        db.refresh(db_book)
    except Exception as e:
        db.rollback()
        raise e
    
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        return None
    
    try:
        db.delete(db_book)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    
    return db_book