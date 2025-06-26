from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import User, Relatorio, UserCreate, RoleEnum, QuestionnaireResponseOut, RelatorioCreate
from app.models import UserRole
from app.crud.nutricionista import get_pacientes, get_relatorios_por_paciente
from app.core.security import get_current_user, require_role
from app.crud.user import get_user_by_email, create_user
from app.crud.questionario import listar_respostas_por_paciente, criar_relatorio


router = APIRouter()

@router.get("/me/pacientes", response_model=List[User])
def list_meus_pacientes(db: Session = Depends(get_db), current_user: User = Depends(require_role("nutricionista"))):
    return get_pacientes(db, current_user.id)

@router.get("/pacientes/{paciente_id}/relatorios", response_model=List[Relatorio])
def list_relatorios(paciente_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_relatorios_por_paciente(db, paciente_id)

@router.post('/relatorios', response_model=Relatorio, status_code=201)
def criar_relatorio_manual(
    data: RelatorioCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("nutricionista"))
):
    return criar_relatorio(
        db=db,
        paciente_id=data.paciente_id,
        nutricionista_id=current_user.id,
        conteudo=data.conteudo
    )

@router.get(
    '/pacientes/{paciente_id}/respostas',
    response_model=List[QuestionnaireResponseOut],
    dependencies=[Depends(require_role("nutricionista"))]
)
def get_respostas_paciente(
    paciente_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return listar_respostas_por_paciente(db, paciente_id)

@router.post("/pacientes", response_model=User, status_code=201)
def cadastrar_paciente(
    paciente_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("nutricionista"))
):
    # Força que o novo usuário será paciente
    paciente_data.role = RoleEnum.paciente

    # Associa ao nutricionista autenticado
    paciente_data.nutricionista_id = current_user.id

    # Evita duplicidade
    if get_user_by_email(db, paciente_data.email):
        raise HTTPException(status_code=400, detail="Email já registrado.")

    return create_user(db, paciente_data)
