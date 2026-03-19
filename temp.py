from app.core.database import SessionLocal
from app.models.books import Book
from app.models. users import User

db = SessionLocal()

books = [
    Book(title="Dac Nhan Tam", author="Dale Carnegie", price = 85000),
    Book(title="Tu Duy Nhanh Va Cham", author="Daniel Kahneman", price=95000),
    Book(title="Nha Gia Kim", author="George S. Clason", price=75000),
    Book(title="Tu Duy Phan Boi", author="Adam Grant", price=90000)
]

user = [
    User()
]

db.add_all(books)
db.commit()
db.close()

print("Data seeded successfully!")