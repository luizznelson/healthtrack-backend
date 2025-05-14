from sqlalchemy.orm import Session
from app.models.questionario import Questionario
from app.schemas.questionario import QuestionarioCreate, QuestionarioOut
from app.services.score import calculate_diabetes_score

def create_questionario(db: Session, paciente_id: int, q_in: QuestionarioCreate):
    scoring = calculate_diabetes_score(q_in)

    q = Questionario(
        paciente_id=paciente_id,

        # valores brutos
        idade               = q_in.idade,
        imc                 = q_in.imc,
        circunferencia      = q_in.circunferencia,
        sexo                = q_in.sexo,
        atividade_fisica    = q_in.atividade_fisica,
        consumo_frutas_diario = q_in.consumo_frutas_diario,
        uso_medicamentos_hipertensao = q_in.uso_medicamentos_hipertensao,
        historico_glicose_alta = q_in.historico_glicose_alta,
        historico_familiar  = q_in.historico_familiar,

        # pontos
        idade_pontos        = scoring["idade"],
        imc_pontos          = scoring["imc"],
        circunferencia_pontos = scoring["circunferencia"],
        atividade_fisica_pontos = scoring["atividade_fisica"],
        habitos_alimentares_pontos = scoring["habitos_alimentares"],
        medicamentos_pontos = scoring["medicamentos"],
        glicose_pontos      = scoring["glicose"],
        familiar_pontos     = scoring["familiar"],

        total_score         = scoring["total"],
        risk_level          = scoring["risk_level"],
    )

    db.add(q)
    db.commit()
    db.refresh(q)
    return QuestionarioOut.from_orm(q)



def get_questionarios_by_paciente(db: Session, paciente_id: int):
    questionarios = db.query(Questionario).filter(Questionario.paciente_id == paciente_id).all()
    
    # Convertendo os objetos ORM para instâncias de Pydantic usando from_orm
    return [QuestionarioOut.from_orm(q) for q in questionarios]
