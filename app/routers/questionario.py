from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    QuestionnaireTemplateCreate,
    QuestionnaireTemplateOut,
    QuestionnaireResponseIn,
    QuestionnaireResponseOut,
    QuestionnaireAnswerOut,
    User,
)
from app.crud.questionario import (
    create_questionnaire_template,
    get_all_templates,
    get_template_by_id,
    compute_score_and_interpretation,
    salvar_resposta,
    listar_respostas_detalhadas_por_resposta
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
    dependencies=[Depends(require_role("nutricionista", "paciente"))],  # ou permita pacientes verem templates?
)
def list_templates(
    db: Session = Depends(get_db),
):
    return get_all_templates(db)

@router.get(
    '/templates/{template_id}',
    response_model=QuestionnaireTemplateOut,
    dependencies=[Depends(require_role("nutricionista", "paciente"))],  # ou role ambos se quiser
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

    response = salvar_resposta(
        db=db,
        template_id=template_id,
        paciente_id=current_user.id,
        total_score=result["total_score"],
        interpretation=result["interpretation"],
        respostas=result["respostas"],
    )
    return response


@router.get(
    "/respostas/{response_id}/detalhes",
    response_model=List[QuestionnaireAnswerOut],
    dependencies=[Depends(require_role("nutricionista", "paciente"))]
)
def detalhes_resposta(
    response_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return listar_respostas_detalhadas_por_resposta(db, response_id)