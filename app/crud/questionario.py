from sqlalchemy.orm import Session
from app.models import QuestionnaireTemplate, QuestionTemplate, OptionTemplate, Questionario, QuestionnaireResponse, QuestionnaireAnswer
from app.schemas import QuestionnaireTemplateCreate, QuestionnaireResponseIn

# CRUD questionários estáticos

def get_questionarios(db: Session, user_id: int):
    return db.query(Questionario).filter(Questionario.owner_id == user_id).all()

def create_questionario(db: Session, user_id: int, data: QuestionnaireResponseIn):
    pass

# CRUD questionários dinâmicos
def create_questionnaire_template(db: Session, data: QuestionnaireTemplateCreate):
    tmpl = QuestionnaireTemplate(title=data.title, description=data.description)
    db.add(tmpl)
    db.flush()
    for q in data.questions:
        question = QuestionTemplate(text=q.text, order=q.order, template_id=tmpl.id)
        db.add(question)
        db.flush()
        for opt in q.options:
            db.add(OptionTemplate(text=opt.text, score=opt.score, is_default=opt.is_default, question_id=question.id))
    db.commit()
    db.refresh(tmpl)
    return tmpl

def listar_respostas_detalhadas_por_resposta(db: Session, response_id: int):
    return (
        db.query(QuestionnaireAnswer)
        .filter(QuestionnaireAnswer.response_id == response_id)
        .all()
    )

def salvar_resposta(
    db: Session,
    template_id: int,
    paciente_id: int,
    total_score: int,
    interpretation: str,
    respostas: list[dict],  # lista com {"question_id", "selected_option_id"}
) -> QuestionnaireResponse:
    # Cria o registro da resposta principal
    response = QuestionnaireResponse(
        template_id=template_id,
        paciente_id=paciente_id,
        total_score=total_score,
        interpretation=interpretation,
    )
    db.add(response)
    db.flush()  # Garante que response.id está disponível antes do commit

    # Salva as respostas individuais
    for r in respostas:
        answer = QuestionnaireAnswer(
            response_id=response.id,
            question_id=r["question_id"],
            selected_option_id=r["selected_option_id"]
        )
        db.add(answer)

    db.commit()
    db.refresh(response)
    return response



def listar_respostas_por_paciente(db: Session, paciente_id: int):
    return (
        db.query(QuestionnaireResponse)
        .filter_by(paciente_id=paciente_id)
        .order_by(QuestionnaireResponse.data_resposta.desc())
        .all()
    )


def criar_relatorio(db: Session, paciente_id: int, nutricionista_id: int, conteudo: str) -> Relatorio:
    relatorio = Relatorio(
        paciente_id=paciente_id,
        nutricionista_id=nutricionista_id,
        conteudo=conteudo
    )
    db.add(relatorio)
    db.commit()
    db.refresh(relatorio)
    return relatorio


def get_all_templates(db: Session):
    return db.query(QuestionnaireTemplate).order_by(QuestionnaireTemplate.id).all()

def get_template_by_id(db: Session, template_id: int):
    return db.query(QuestionnaireTemplate).filter(QuestionnaireTemplate.id == template_id).first()

def compute_score_and_interpretation(db: Session, template_id: int, answers: QuestionnaireResponseIn):
    template = get_template_by_id(db, template_id)
    if not template:
        return None

    total = 0
    respostas_salvas = [] 

    for ans in answers.answers:
        opt = db.query(OptionTemplate).filter(
            OptionTemplate.id == ans.option_id,
            OptionTemplate.question_id == ans.question_id
        ).first()

        if opt:
            total += opt.score
            respostas_salvas.append({
                "question_id": ans.question_id,
                "selected_option_id": ans.option_id
            })

    # 🧠 Interpretação dinâmica por questionário
    title = template.title.lower()

    if "diabetes" in title:
        if total <= 5:
            interp = 'Baixo risco de desenvolver diabetes.'
        elif total <= 11:
            interp = 'Risco moderado de desenvolver diabetes.'
        else:
            interp = 'Alto risco de desenvolver diabetes.'

    elif "hipertensão" in title:
        if total <= 4:
            interp = 'Baixo risco de desenvolver hipertensão.'
        elif total <= 9:
            interp = 'Risco moderado de desenvolver hipertensão.'
        elif total <= 15:
            interp = 'Alto risco de desenvolver hipertensão.'
        else:
            interp = 'Risco muito alto de desenvolver hipertensão.'

    else:
        interp = f'Score total: {total}. Nenhuma regra de interpretação cadastrada para \"{template.title}\".'

    return {
        'template_id': template_id,
        'total_score': total,
        'interpretation': interp,
        'respostas': respostas_salvas
    }


