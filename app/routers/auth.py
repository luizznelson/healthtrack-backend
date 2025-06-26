from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.database import get_db
from app.schemas import UserCreate, User, Token
from app.crud.user import (
    create_user,
    get_user_by_email,
    authenticate_user,
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    oauth2_scheme,
    blacklist_token,
)
from app.core.config import settings

router = APIRouter(tags=["auth"])


# ✅ Registro de usuário
@router.post(
    "/register",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo usuário (paciente ou nutricionista)"
)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    if get_user_by_email(db, user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado.",
        )
    return create_user(db, user_in)


# ✅ Geração de tokens (login)
@router.post(
    "/token",
    response_model=Token,
    summary="Gera access e refresh tokens"
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # ⚠️ form_data.username aqui é o email do usuário
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(user.email)
    refresh_token = create_refresh_token(user.email)

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


# ✅ Refresh token
@router.post(
    "/refresh",
    response_model=Token,
    summary="Gera novos tokens a partir de um refresh token válido"
)
def refresh(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token não é do tipo refresh."
            )

        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido."
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não foi possível validar o refresh token."
        )

    blacklist_token(token)

    return Token(
        access_token=create_access_token({"sub": username}),
        refresh_token=create_refresh_token({"sub": username}),
        token_type="bearer"
    )


# ✅ Logout — Revoga o token atual
@router.post(
    "/logout",
    summary="Revoga o token de acesso atual"
)
def logout(token: str = Depends(oauth2_scheme)):
    blacklist_token(token)
    return {"message": "Logout realizado com sucesso."}


# ✅ Dados do usuário logado
@router.get(
    "/me",
    response_model=User,
    summary="Retorna os dados do usuário logado"
)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
