import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.core.security import get_password_hash

def seed():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    if not db.query(User).filter(User.email == "admin@healthtrack.com").first():
        admin = User(
            name="Admin",
            email="admin@healthtrack.com",
            hashed_password=get_password_hash("admin123"),
            role="nutritionist"
        )
        db.add(admin)
        db.commit()
    db.close()

if __name__ == "__main__":
    seed()
    print("Seed completed")
