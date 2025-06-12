from sqlalchemy.orm import Session
from app.models import QuestionnaireTemplate, QuestionTemplate, OptionTemplate, Questionario
from app.schemas import QuestionnaireTemplateCreate, QuestionnaireResponseIn

# CRUD questionários estáticos

def get_questionarios(db: Session, user_id: int):
    return db.query(Questionario).filter(Questionario.owner_id == user_id).all()

def create_questionario(db: Session, user_id: int, data: QuestionnaireResponseIn):
    # funcionalidade legada opcional
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

def get_all_templates(db: Session):
    return db.query(QuestionnaireTemplate).order_by(QuestionnaireTemplate.id).all()

def get_template_by_id(db: Session, template_id: int):
    return db.query(QuestionnaireTemplate).filter(QuestionnaireTemplate.id == template_id).first()

def compute_score_and_interpretation(db: Session, template_id: int, answers: QuestionnaireResponseIn):
    template = get_template_by_id(db, template_id)
    if not template:
        return None
    total = 0
    for ans in answers.answers:
        opt = db.query(OptionTemplate).filter(
            OptionTemplate.id == ans.option_id,
            OptionTemplate.question_id == ans.question_id
        ).first()
        if opt:
            total += opt.score
    if total <= 5:
        interp = 'Baixo risco de desenvolver diabetes.'
    elif total <= 11:
        interp = 'Risco moderado de desenvolver diabetes.'
    else:
        interp = 'Alto risco de desenvolver diabetes.'
    return {
        'template_id': template_id,
        'total_score': total,
        'interpretation': interp
    }