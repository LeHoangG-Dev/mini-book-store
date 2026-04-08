from sqlalchemy.orm import Session
from app.models.users import User
from app.core.database import SessionLocal
from app.core.security import hash_password
from app.core.config import settings
from datetime import datetime, timezone

def create_first_admin():

    db: Session = SessionLocal()

    existing_admin = db.query(User).filter(User.email == settings.admin_email).first()
    if existing_admin:
        print(f"Admin {settings.admin_email} already exists. Skipping creation.")
        return
    
    admin_user = User(
        email=settings.admin_email,
        username="Admin",
        hashed_password=hash_password(settings.admin_password),
        full_name = "Admin User",
        role = "admin",
        is_active=True,
        is_verified=False,
        updated_at=datetime.now(timezone.utc)
    )
    db.add(admin_user)
    db.commit()
    print(f"Admin {settings.admin_email} created successfully.")

