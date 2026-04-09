# tests/test_auth.py
import pytest
from app.services import auth as auth_service
from app.schemas.auth import RegisterRequest, LoginRequest, RefreshTokenRequest, RevokeTokenRequest

# ===========================
# UNIT TESTS (5)
# ===========================

def test_register_success(db_session):
    """Service tạo user thành công, trả về đúng fields"""
    payload = RegisterRequest(
        email="unit@test.com",
        username="unituser",
        password="password123"
    )
    result = auth_service.register(db_session, payload)

    assert result["email"] == "unit@test.com"
    assert result["message"] == "Registration successful"
    assert "access_token" in result
    assert "refresh_token" in result


def test_register_duplicate_email_raises(db_session):
    """Service raise ValueError khi email đã tồn tại"""
    payload = RegisterRequest(
        email="dup@test.com",
        username="dupuser",
        password="password123"
    )
    auth_service.register(db_session, payload)

    with pytest.raises(ValueError, match="Email already exists"):
        auth_service.register(db_session, RegisterRequest(
            email="dup@test.com",
            username="dupuser2",
            password="password123"
        ))


def test_register_duplicate_username_raises(db_session):
    """Service raise ValueError khi username đã tồn tại"""
    auth_service.register(db_session, RegisterRequest(
        email="user1@test.com",
        username="sameusername",
        password="password123"
    ))

    with pytest.raises(ValueError, match="Username already exists"):
        auth_service.register(db_session, RegisterRequest(
            email="user2@test.com",
            username="sameusername",
            password="password123"
        ))


def test_login_wrong_password_raises(db_session):
    """Service raise ValueError khi sai password"""
    auth_service.register(db_session, RegisterRequest(
        email="login@test.com",
        username="loginuser",
        password="password123"
    ))

    with pytest.raises(ValueError, match="Invalid email or password"):
        auth_service.login(db_session, LoginRequest(
            email="login@test.com",
            password="wrongpassword"
        ))


def test_logout_revokes_token(db_session):
    """Service logout đánh dấu token is_revoked = True"""
    from app.models.auth import RefreshToken

    result = auth_service.register(db_session, RegisterRequest(
        email="logout@test.com",
        username="logoutuser",
        password="password123"
    ))

    auth_service.logout(db_session, RevokeTokenRequest(
        refresh_token=result["refresh_token"]
    ))

    db_token = db_session.query(RefreshToken).filter(
        RefreshToken.token == result["refresh_token"]
    ).first()
    assert db_token.is_revoked is True


