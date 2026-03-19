from fastapi import APIRouter, status, Depends, HTTPException
from app.schemas.auth import RegisterResponse, RegisterRequest, LoginRequest, RefreshTokenRequest, LoginResponse, RefreshTokenResponse, RevokeTokenRequest
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.services import auth
from app.schemas.users import MessageResponse

router = APIRouter()

@router.post("/register", response_model = RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(register_reqquest: RegisterRequest, db: Session = Depends(get_db)):
    
    try:
        user = auth.register(db, register_reqquest)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return user


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    try:
        return auth.login(db, login_request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = str(e))
    
@router.post("/refresh", status_code=status.HTTP_200_OK)
def refresh(refresh_token_request: RefreshTokenRequest, db: Session = Depends(get_db)):
    try:
        return auth.refresh(db, refresh_token_request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    


@router.post("/logout", response_model=MessageResponse, status_code=status.HTTP_200_OK)
def logout(revoke_request: RevokeTokenRequest, db: Session = Depends(get_db)):
    try:
        auth.logout(db, revoke_request)
    except ValueError as e :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = str(e))
    
    return {"message": "Log out successfully"}