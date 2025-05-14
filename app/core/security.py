<<<<<<< Updated upstream
=======
from sqlalchemy.orm import Session  # Adicione essa importação
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
>>>>>>> Stashed changes
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.config import settings
from app.schemas.user import TokenData
<<<<<<< Updated upstream
=======
from app.database import get_db  # Certifique-se de que get_db está sendo importado
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Exceção padrão para credenciais inválidas
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
>>>>>>> Stashed changes

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_access_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        return TokenData(email=email)
    except JWTError:
        return TokenData()
<<<<<<< Updated upstream
=======

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")  # 'sub' contém o email, e não o id
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)  # Passando apenas o email para TokenData
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == token_data.email).first()  # Busca pelo email
    if user is None:
        raise credentials_exception
    return user
>>>>>>> Stashed changes
