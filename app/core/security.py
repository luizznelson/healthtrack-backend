from datetime import datetime, timedelta
from typing import Optional, Set
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud.user import get_user_by_email
from app.database import get_db
from app.schemas import User

# 🔐 OAuth2 Config
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# 🔒 Lista de tokens revogados
_blacklisted_tokens: Set[str] = set()


# 🔐 Blacklist
def blacklist_token(token: str):
    _blacklisted_tokens.add(token)


def is_token_blacklisted(token: str) -> bool:
    return token in _blacklisted_tokens


# 🔥 Gerar Access Token
def create_access_token(subject: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": subject,
        "exp": expire,
        "type": "access"
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# 🔥 Gerar Refresh Token
def create_refresh_token(subject: str) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {
        "sub": subject,
        "exp": expire,
        "type": "refresh"
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# 🔑 Obter usuário atual a partir do token
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    if is_token_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token revogado. Faça login novamente."
        )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido para este tipo de acesso."
            )

        username: Optional[str] = payload.get("sub")
        if not username:
            raise ValueError("Token sem username")

    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não foi possível validar as credenciais."
        )

    user = get_user_by_email(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    return user


# 🔐 Controle de acesso por papéis (roles)
def require_role(*allowed_roles: str):
    def role_checker(current_user: User = Depends(get_current_user)):
        role_value = (
            current_user.role.value if hasattr(current_user.role, "value") else current_user.role
        )

        if role_value not in allowed_roles:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                detail="Acesso negado para este recurso."
            )
        return current_user
    return role_checker