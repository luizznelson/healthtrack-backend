from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    QuestionnaireTemplateCreate,
    QuestionnaireTemplateOut,
    QuestionnaireResponseIn,
    QuestionnaireResponseOut,
    User,
)
from app.crud.questionario import (
    create_questionnaire_template,
    get_all_templates,
    get_template_by_id,
    compute_score_and_interpretation,
)
from app.core.security import get_current_user, require_role

router = APIRouter()

# Templates (somente nutricionista)
@router.post(
    '/templates',
    response_model=QuestionnaireTemplateOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("nutricionista"))],
)
def create_template(
    data: QuestionnaireTemplateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_questionnaire_template(db, data)

@router.get(
    '/templates',
    response_model=List[QuestionnaireTemplateOut],
    dependencies=[Depends(require_role("nutricionista"))],  # ou permita pacientes verem templates?
)
def list_templates(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_all_templates(db)

@router.get(
    '/templates/{template_id}',
    response_model=QuestionnaireTemplateOut,
    dependencies=[Depends(require_role("nutricionista"))],  # ou role ambos se quiser
)
def get_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tmpl = get_template_by_id(db, template_id)
    if not tmpl:
        raise HTTPException(status_code=404, detail='Template não encontrado')
    return tmpl

# Respostas (somente paciente)
@router.post(
    '/{template_id}/respostas',
    response_model=QuestionnaireResponseOut,
    dependencies=[Depends(require_role("paciente"))],
)
def submit_response(
    template_id: int,
    payload: QuestionnaireResponseIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = compute_score_and_interpretation(db, template_id, payload)
    if not result:
        raise HTTPException(status_code=404, detail='Template não encontrado')
    return result

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

