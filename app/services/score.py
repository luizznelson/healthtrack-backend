from app.schemas.questionario import QuestionarioBase

def calculate_diabetes_score(data: QuestionarioBase) -> dict:
    # 1) idade
    if data.idade < 45:
        pts_idade = 0
    elif data.idade <= 54:
        pts_idade = 2
    elif data.idade <= 64:
        pts_idade = 3
    else:
        pts_idade = 4

    # 2) IMC
    if data.imc < 25:
        pts_imc = 0
    elif data.imc < 30:
        pts_imc = 1
    else:
        pts_imc = 3

    # 3) circunferência abdominal
    if data.sexo == "Masculino":
        if data.circunferencia < 94:
            pts_circ = 0
        elif data.circunferencia <= 102:
            pts_circ = 3
        else:
            pts_circ = 4
    else:  # Feminino
        if data.circunferencia < 80:
            pts_circ = 0
        elif data.circunferencia <= 88:
            pts_circ = 3
        else:
            pts_circ = 4

    # 4) atividade física
    pts_atividade = 0 if data.atividade_fisica else 2

    # 5) consumo diário de frutas/verduras
    pts_habitos = 0 if data.consumo_frutas_diario else 1

    # 6) uso de medicamentos para hipertensão
    pts_medic = 2 if data.uso_medicamentos_hipertensao else 0

    # 7) histórico de glicose alta
    pts_glicose = 5 if data.historico_glicose_alta else 0

    # 8) histórico familiar
    if data.historico_familiar == "Nenhum":
        pts_fam = 0
    elif data.historico_familiar == "Avós/Tios":
        pts_fam = 3
    else:  # Pais/Irmãos
        pts_fam = 5

    total = sum([pts_idade, pts_imc, pts_circ, pts_atividade,
                 pts_habitos, pts_medic, pts_glicose, pts_fam])

    if total <= 5:
        nivel = "Baixo"
    elif total <= 11:
        nivel = "Moderado"
    else:
        nivel = "Alto"

    return {
        "idade": pts_idade,
        "imc": pts_imc,
        "circunferencia": pts_circ,
        "atividade_fisica": pts_atividade,
        "habitos_alimentares": pts_habitos,
        "medicamentos": pts_medic,
        "glicose": pts_glicose,
        "familiar": pts_fam,
        "total": total,
        "risk_level": nivel
    }
