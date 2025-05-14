from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Numeric, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Questionario(Base):
    __tablename__ = "questionarios"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # **Campos brutos**
    idade               = Column(Integer, nullable=False)
    imc                 = Column(Numeric(5,2), nullable=False)
    circunferencia      = Column(Numeric(5,2), nullable=False)
    sexo                = Column(String, nullable=False)
    atividade_fisica    = Column(Boolean, nullable=False)
    consumo_frutas_diario = Column(Boolean, nullable=False)
    uso_medicamentos_hipertensao = Column(Boolean, nullable=False)
    historico_glicose_alta = Column(Boolean, nullable=False)
    historico_familiar  = Column(String, nullable=False)

    # **Campos de pontuação**
    idade_pontos        = Column(Integer, nullable=False)
    imc_pontos          = Column(Integer, nullable=False)
    circunferencia_pontos = Column(Integer, nullable=False)
    atividade_fisica_pontos = Column(Integer, nullable=False)
    habitos_alimentares_pontos = Column(Integer, nullable=False)
    medicamentos_pontos = Column(Integer, nullable=False)
    glicose_pontos      = Column(Integer, nullable=False)
    familiar_pontos     = Column(Integer, nullable=False)

    total_score         = Column(Integer, nullable=False)
    risk_level          = Column(String, nullable=False)

    paciente = relationship("User", back_populates="questionarios")


