from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models import User
from app.schemas import UserCreate

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user_in: UserCreate):
    """
    Cria um usuário a partir de um UserCreate.
    """
    # Hash da senha
    hashed = pwd_context.hash(user_in.password)
    db_user = User(
        username=user_in.username,
        hashed_password=hashed,
        role=user_in.role  # RoleEnum vindo do schema
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not pwd_context.verify(password, user.hashed_password):
        return None
    return user