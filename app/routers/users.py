from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
from ..schemas.users import UserCreate, UserResponse, UserUpdate, ChangePasswordRequest
from app.core.dependencies import get_db
from sqlalchemy.orm import Session
from app.services.users import get_all_users, register_user, get_user_by_id, update_profile, change_user_password
from app.core.dependencies import require_admin, require_role, require_user, get_current_user
from app.models.users import User

router = APIRouter()

@router.get("/",response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    return get_all_users(db)

@router.get("/me",response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_me(current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return current_user


@router.put("/me", response_model=UserResponse,status_code=status.HTTP_200_OK)
def update_me(
    user: UserUpdate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_updated = update_profile(db,current_user.id,user)
    if not user_updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_updated

@router.put("/me/password", response_model=UserResponse, status_code=status.HTTP_200_OK)
def change_password(password_change: ChangePasswordRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return change_user_password(db, current_user.id, password_change)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    





