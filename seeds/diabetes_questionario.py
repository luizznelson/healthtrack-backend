from app.database import SessionLocal
from app.models import QuestionnaireTemplate, QuestionTemplate, OptionTemplate

db = SessionLocal()

# Verifica se já existe
existing = db.query(QuestionnaireTemplate).filter_by(title="Avaliação de Risco de Diabetes").first()
if existing:
    print("Questionário de Diabetes já existe.")
    exit(0)

# Dados do questionário
questionnaire = QuestionnaireTemplate(
    title="Avaliação de Risco de Diabetes",
    description="Questionário para estimar o risco de desenvolver diabetes tipo 2."
)

db.add(questionnaire)
db.flush()

questions_data = [
    {
        "text": "Idade",
        "order": 1,
        "options": [
            ("Menos de 45 anos", 0),
            ("Entre 45 e 54 anos", 2),
            ("Entre 55 e 64 anos", 3),
            ("65 anos ou mais", 4),
        ]
    },
    {
        "text": "Índice de Massa Corporal (IMC)",
        "order": 2,
        "options": [
            ("Menos de 25", 0),
            ("Entre 25 e 30", 1),
            ("30 ou mais", 3),
        ]
    },
    {
        "text": "Circunferência Abdominal (Homens)",
        "order": 3,
        "options": [
            ("Menos de 94 cm", 0),
            ("Entre 94 e 102 cm", 3),
            ("Mais de 102 cm", 4),
        ]
    },
    {
        "text": "Circunferência Abdominal (Mulheres)",
        "order": 4,
        "options": [
            ("Menos de 80 cm", 0),
            ("Entre 80 e 88 cm", 3),
            ("Mais de 88 cm", 4),
        ]
    },
    {
        "text": "Atividade Física Regular (mínimo de 30 minutos por dia)",
        "order": 5,
        "options": [
            ("Sim", 0),
            ("Não", 2),
        ]
    },
    {
        "text": "Consumo Regular de Frutas, Verduras e Legumes",
        "order": 6,
        "options": [
            ("Sim, todos os dias", 0),
            ("Não, menos de uma vez por dia", 1),
        ]
    },
    {
        "text": "Uso de Medicamentos para Hipertensão",
        "order": 7,
        "options": [
            ("Não", 0),
            ("Sim", 2),
        ]
    },
    {
        "text": "Histórico de Glicose Alta no Sangue",
        "order": 8,
        "options": [
            ("Não", 0),
            ("Sim", 5),
        ]
    },
    {
        "text": "Histórico Familiar de Diabetes",
        "order": 9,
        "options": [
            ("Não", 0),
            ("Sim: Avós, tios", 3),
            ("Sim: Pais, irmãos", 5),
        ]
    },
]

# Cria perguntas e opções
for q in questions_data:
    question = QuestionTemplate(
        text=q["text"],
        order=q["order"],
        template_id=questionnaire.id
    )
    db.add(question)
    db.flush()

    for option_text, score in q["options"]:
        option = OptionTemplate(
            text=option_text,
            score=score,
            question_id=question.id
        )
        db.add(option)

db.commit()
db.refresh(questionnaire)
print(f"✅ Questionário '{questionnaire.title}' criado com sucesso!")
