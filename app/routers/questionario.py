from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.questionario import QuestionarioCreate, QuestionarioOut
import app.crud.questionario as crud_q
from app.core.security import get_current_user

router = APIRouter(prefix="/pacientes/{paciente_id}/questionarios", tags=["questionarios"])

@router.post("/", response_model=QuestionarioOut, status_code=status.HTTP_201_CREATED)
def create_questionario(
    paciente_id: int,
    q_in: QuestionarioCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # somente o próprio paciente ou nutricionista podem criar
    if current_user.role == "paciente" and current_user.id != paciente_id:
        raise HTTPException(status_code=403, detail="Acesso negado")
    return crud_q.create_questionario(db, paciente_id, q_in)

@router.get("/", response_model=List[QuestionarioOut])
def list_questionarios(
    paciente_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.role == "paciente" and current_user.id != paciente_id:
        raise HTTPException(status_code=403, detail="Acesso negado")
    return crud_q.get_questionarios_by_paciente(db, paciente_id)
