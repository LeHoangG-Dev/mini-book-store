
    

"""
@pytest.fixture
def registered_user(client):
    res = client.post("/api/v1/auth/register", json={
        "email": "test@test.com",
        "password": "12345678",
        "full_name": "Test User"
    })
    return res.json()

@pytest.fixture
def token(client, registered_user):
    res = client.post("/api/v1/auth/login", json={
        "email": "test@test.com",
        "password": "12345678"
    })
    return res.json()["access_token"]

@pytest.fixture
def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def category(client, auth_headers):
    res = client.post("/api/v1/categories/", 
        json={"name": "Fiction"},
        headers=auth_headers
    )
    return res.json()

@pytest.fixture
def book(client, auth_headers, category):
    res = client.post("/api/v1/books/",
        json={
            "title": "Test Book",
            "author": "Author",
            "price": 100.0,
            "category_id": category["id"]
        },
        headers=auth_headers
    )
    return res.json()
"""