from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
from app.schemas.user import UserCreate, UserOut, Token
from app.services.authentication import register_user, authenticate_user, generate_token
from app.core.exceptions import credentials_exception
from app import crud

<<<<<<< Updated upstream
router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user_in)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
=======
# Definir a URL do OAuth2
router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # Registra o usuário
    return register_user(db, user_in)

@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Verifica as credenciais do usuário
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Gera o token para o usuário
>>>>>>> Stashed changes
    access_token = generate_token(user)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserOut)
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
<<<<<<< Updated upstream
    from app.core.security import decode_access_token
    token_data = decode_access_token(token)
    if not token_data.email:
        raise credentials_exception
    user = crud.get_user_by_email(db, token_data.email)
    if not user:
        raise credentials_exception
=======
    # Decodifica o token para pegar o email
    from app.core.security import decode_access_token
    token_data = decode_access_token(token)
    
    # Verifica se o email existe no token
    if not token_data.email:
        raise credentials_exception
    
    # Busca o usuário no banco de dados
    user = crud.get_user_by_email(db, token_data.email)
    if not user:
        raise credentials_exception
    
>>>>>>> Stashed changes
    return user
