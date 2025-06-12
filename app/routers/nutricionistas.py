from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import User, Relatorio
from app.crud.nutricionista import get_pacientes, get_relatorios_por_paciente
from app.core.security import get_current_user

router = APIRouter()

@router.get("/{nutricionista_id}/pacientes", response_model=List[User])
def list_pacientes(nutricionista_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_pacientes(db, nutricionista_id)

@router.get("/pacientes/{paciente_id}/relatorios", response_model=List[Relatorio])
def list_relatorios(paciente_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_relatorios_por_paciente(db, paciente_id)