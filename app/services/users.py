from sqlalchemy.orm import Session
from app.models.users import User
from app.schemas.users import UserCreate, UserUpdate, UserResponse, ChangePasswordRequest, MessageResponse
from app.core.security import hash_password, verify_password
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_all_users(db: Session):
    return db.query(User).all()

def register_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User(
        **user.model_dump(exclude={"password"}),
        hashed_password=hashed_password
    )
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        raise e
    return db_user

def update_profile(db: Session, user_id: int, user_update: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    
    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)

    try:    
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        raise e
    
    return db_user

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def change_user_password(db: Session, user_id: int, change_password: ChangePasswordRequest):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    
    if not verify_password(change_password.old_password, db_user.hashed_password):
        raise ValueError("Old password is incorrect")
    
    db_user.hashed_password = hash_password(change_password.new_password)

    try:
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        raise e
    
    return db_user
