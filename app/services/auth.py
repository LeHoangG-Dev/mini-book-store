from app.schemas.auth import RegisterRequest, LoginRequest, RefreshTokenRequest, RevokeTokenRequest
from sqlalchemy.orm import Session
from app.models.users import User, UserRole
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.models.auth import RefreshToken
from app.core.config import settings
from datetime import datetime, timedelta, timezone

def register(db: Session, register_request: RegisterRequest):
    if db.query(User).filter(User.email == register_request.email).first():
        raise ValueError("Email already exists")
    

    if db.query(User).filter(User.username == register_request.username).first():
        raise ValueError("Username already exists")
    
    user = User(
        email=register_request.email,
        username=register_request.username,
        hashed_password=hash_password(register_request.password),
        full_name=register_request.full_name
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(user.id, user.role)
    refresh_token_str = create_refresh_token(user.id)

    db_token = RefreshToken(
        user_id=user.id,
        token=refresh_token_str,
        expires_at=datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
    )
    db.add(db_token)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token_str,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email,
        "message": "Registration successful"
    }

def login(db: Session, login_request: LoginRequest):
    user = db.query(User).filter(User.email == login_request.email).first()
    if not user or not verify_password(login_request.password, user.hashed_password):
        raise ValueError("Invalid email or password")
    
    access_token = create_access_token(user.id, user.role)
    refresh_token_str = create_refresh_token(user.id)

    db_token = RefreshToken(
        user_id=user.id,
        token=refresh_token_str,
        expires_at=datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)

    )
    db.add(db_token)
    db.commit()

    return {
    "access_token": access_token,
    "refresh_token": refresh_token_str,
    "token_type": "bearer",
    "user_id": user.id,
    "email": user.email
    }

def refresh(db: Session, refresh_token_request: RefreshTokenRequest):
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token_request.refresh_token,
        RefreshToken.is_revoked == False
    ).first()

    if not db_token or db_token.expires_at < datetime.now(timezone.utc).replace(tzinfo=None):
        raise ValueError("Invalid or expired refresh token")
    
    access_token = create_access_token(db_token.user_id)
    return {"access_token": access_token}

def logout(db: Session, data: RevokeTokenRequest):
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == data.refresh_token
    ).first()

    if not db_token:
        raise ValueError("Token not found")
    
    db_token.is_revoked = True
    db.commit()