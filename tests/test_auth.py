# tests/test_auth.py

def test_register(client):
    res = client.post("/api/v1/auth/register", json={
        "email": "new@test.com",
        "password": "12345678",
        "full_name": "New User"
    })
    assert res.status_code == 201

def test_register_duplicate_email(client, registered_user):
    res = client.post("/api/v1/auth/register", json={
        "email": "test@test.com",
        "password": "12345678",
        "full_name": "Test User"
    })
    assert res.status_code == 400

def test_login(client, registered_user):
    res = client.post("/api/v1/auth/login", json={
        "email": "test@test.com",
        "password": "12345678"
    })
    assert res.status_code == 200
    assert "access_token" in res.json()

def test_login_wrong_password(client, registered_user):
    res = client.post("/api/v1/auth/login", json={
        "email": "test@test.com",
        "password": "wrongpass"
    })
    assert res.status_code == 401