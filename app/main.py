from fastapi import FastAPI
from .routers import auth, books, cart, categories, orders, reviews, users
from .models import User, RefreshToken, Book
app = FastAPI()

@app.get("/", tags=["Health"])
def root():
    return {"Message": "Hello"}

app.include_router(auth.router, prefix = "/api/v1/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(books.router, prefix="/api/v1/books", tags=["Books"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["Categories"])
app.include_router(cart.router, prefix="/api/v1/cart", tags=["Cart"])
app.include_router(orders.router, prefix="/api/v1/orders", tags=["Orders"])
app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["Reviews"])
"""
1 Books
2 Users
3 Auth
4 Categories
5 cart
6 orders
7 reviews
"""