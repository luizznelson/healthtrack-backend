from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.crud.user import get_user_by_email, create_user
from app.schemas.user import UserCreate
from app.core.security import verify_password, create_access_token

def register_user(db: Session, user_in: UserCreate):
    if get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user_in)

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def generate_token(user):
    return create_access_token({"sub": user.email})
