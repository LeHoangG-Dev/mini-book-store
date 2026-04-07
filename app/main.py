from fastapi import FastAPI
from .routers import auth, books, cart, orders, users
from .models import User, RefreshToken, Book
from app.core.create_admin import create_first_admin

create_first_admin()

app = FastAPI()

@app.get("/", tags=["Health"])
def root():
    return {"Message": "Hello"}

app.include_router(auth.router, prefix = "/api/v1/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(books.router, prefix="/api/v1/books", tags=["Books"])
app.include_router(cart.router, prefix="/api/v1/cart", tags=["Cart"])
app.include_router(orders.router, prefix="/api/v1/orders", tags=["Orders"])

