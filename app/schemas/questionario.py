from pydantic import BaseModel, condecimal, validator
from typing import Literal
import datetime

class QuestionarioBase(BaseModel):
    idade: int                        # em anos
    imc: condecimal(gt=0, lt=100)
    circunferencia: condecimal(gt=0, lt=300)
    sexo: Literal["Masculino", "Feminino"]
    atividade_fisica: bool
    consumo_frutas_diario: bool
    uso_medicamentos_hipertensao: bool
    historico_glicose_alta: bool
    historico_familiar: Literal["Nenhum", "Avós/Tios", "Pais/Irmãos"]

    @validator("idade")
    def idade_nao_negativa(cls, v):
        if v < 0 or v > 120:
            raise ValueError("Idade deve ser entre 0 e 120")
        return v

class QuestionarioCreate(QuestionarioBase):
    pass

class QuestionarioOut(BaseModel):
    # idade: int
    # imc: float
    # circunferencia: float
    # sexo: Literal["Masculino", "Feminino"]
    # atividade_fisica: bool
    # consumo_frutas_diario: bool
    # uso_medicamentos_hipertensao: bool
    # historico_glicose_alta: bool
    # historico_familiar: Literal["Nenhum", "Avós/Tios", "Pais/Irmãos"]
    # id: int
    # created_at: datetime.datetime
    total_score: int
    risk_level: Literal["Baixo", "Moderado", "Alto"]

    class Config:
        orm_mode = True
        from_attributes = True

