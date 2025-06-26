from app.database import SessionLocal
from app.models import QuestionnaireTemplate, QuestionTemplate, OptionTemplate

db = SessionLocal()

# Verifica se já existe
existing = db.query(QuestionnaireTemplate).filter_by(title="Avaliação de Risco de Hipertensão").first()
if existing:
    print("Questionário de Hipertensão já existe.")
    exit(0)

# Criação do template
questionnaire = QuestionnaireTemplate(
    title="Avaliação de Risco de Hipertensão",
    description="Questionário para estimar o risco de desenvolver hipertensão."
)
db.add(questionnaire)
db.flush()

questions_data = [
    {
        "text": "Idade",
        "order": 1,
        "options": [
            ("Menos de 40 anos", 0),
            ("Entre 40 e 49 anos", 1),
            ("Entre 50 e 59 anos", 2),
            ("60 anos ou mais", 3),
        ]
    },
    {
        "text": "Índice de Massa Corporal (IMC)",
        "order": 2,
        "options": [
            ("Menos de 25", 0),
            ("Entre 25 e 30", 1),
            ("30 ou mais", 2),
        ]
    },
    {
        "text": "Consumo de Sal (autoavaliação)",
        "order": 3,
        "options": [
            ("Baixo", 0),
            ("Moderado", 1),
            ("Alto", 2),
        ]
    },
    {
        "text": "Atividade Física Regular",
        "order": 4,
        "options": [
            ("Sim, regularmente", 0),
            ("Não, pouco ou nenhum exercício", 2),
        ]
    },
    {
        "text": "Consumo de Álcool",
        "order": 5,
        "options": [
            ("Não consumo", 0),
            ("Consumo leve a moderado", 1),
            ("Consumo excessivo", 3),
        ]
    },
    {
        "text": "Histórico Familiar de Hipertensão",
        "order": 6,
        "options": [
            ("Não", 0),
            ("Sim, com histórico em familiares de segundo grau", 1),
            ("Sim, com histórico em familiares de primeiro grau", 2),
        ]
    },
    {
        "text": "Estresse no Dia a Dia",
        "order": 7,
        "options": [
            ("Baixo", 0),
            ("Moderado", 1),
            ("Alto", 2),
        ]
    },
    {
        "text": "Consumo de Alimentos Ultraprocessados",
        "order": 8,
        "options": [
            ("Raramente", 0),
            ("Moderado", 1),
            ("Frequentemente", 2),
        ]
    },
    {
        "text": "Tabagismo",
        "order": 9,
        "options": [
            ("Nunca fumei", 0),
            ("Parei de fumar há mais de um ano", 1),
            ("Parei de fumar há menos de um ano", 2),
            ("Fumo atualmente", 3),
        ]
    },
    {
        "text": "Pressão Arterial Elevada em Exames Recentes",
        "order": 10,
        "options": [
            ("Não", 0),
            ("Sim, uma vez", 1),
            ("Sim, mais de uma vez", 3),
        ]
    },
]

# Inserção das perguntas e opções
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
