from enum import Enum as PyEnum
from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Text,
    Boolean, Enum as SqlEnum
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from zoneinfo import ZoneInfo

Base = declarative_base()

def now_brazil():
    return datetime.now(ZoneInfo("America/Sao_Paulo"))

class UserRole(PyEnum):
    paciente = 'paciente'
    nutricionista = 'nutricionista'

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=True) 
    email = Column(String, unique=True, index=True, nullable=False) 
    hashed_password = Column(String, nullable=False)
    role = Column(SqlEnum(UserRole), default=UserRole.paciente)

    # Relações legadas
    nutricionista_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    # Relacionamento reverso (acesso ao nutricionista que cadastrou o paciente)
    nutricionista = relationship("User", remote_side=[id])
    questionarios = relationship('Questionario', back_populates='owner', cascade='all, delete-orphan')
    relatorios_paciente = relationship('Relatorio', back_populates='paciente', foreign_keys='Relatorio.paciente_id')
    relatorios_nutricionista = relationship('Relatorio', back_populates='nutricionista', foreign_keys='Relatorio.nutricionista_id')

class Questionario(Base):
    __tablename__ = 'questionarios'
    id = Column(Integer, primary_key=True, index=True)
    respostas = Column(Text)          # conforme seu schema legado
    data = Column(DateTime, default=now_brazil)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    owner = relationship(
        'User',
        back_populates='questionarios',
        foreign_keys=[owner_id]
    )

class Relatorio(Base):
    __tablename__ = 'relatorios'

    id = Column(Integer, primary_key=True, index=True)
    conteudo = Column(Text)
    paciente_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    nutricionista_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    data_criacao = Column(DateTime, default=now_brazil)

    paciente = relationship(
        'User',
        back_populates='relatorios_paciente',
        foreign_keys=[paciente_id]
    )
    nutricionista = relationship(
        'User',
        back_populates='relatorios_nutricionista',
        foreign_keys=[nutricionista_id]
    )

class QuestionnaireResponse(Base):
    __tablename__ = "questionnaire_responses"

    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("questionnaire_templates.id"), nullable=False)
    paciente_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_score = Column(Integer, nullable=False)
    interpretation = Column(Text, nullable=False)
    data_resposta = Column(DateTime, default=now_brazil)

    paciente = relationship("User", foreign_keys=[paciente_id])
    template = relationship("QuestionnaireTemplate", foreign_keys=[template_id])

# Models dinâmicos para questionários
class QuestionnaireTemplate(Base):
    __tablename__ = 'questionnaire_templates'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    questions = relationship('QuestionTemplate', back_populates='template', cascade='all, delete')

class QuestionTemplate(Base):
    __tablename__ = 'question_templates'
    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey('questionnaire_templates.id', ondelete='CASCADE'))
    text = Column(String, nullable=False)
    order = Column(Integer, nullable=False)
    options = relationship('OptionTemplate', back_populates='question', cascade='all, delete')
    template = relationship('QuestionnaireTemplate', back_populates='questions')

class OptionTemplate(Base):
    __tablename__ = 'option_templates'
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey('question_templates.id', ondelete='CASCADE'))
    text = Column(String, nullable=False)
    score = Column(Integer, nullable=False, default=0)
    is_default = Column(Boolean, default=False)
    question = relationship('QuestionTemplate', back_populates='options')
    
class QuestionnaireAnswer(Base):
    __tablename__ = "questionnaire_answers"

    id = Column(Integer, primary_key=True, index=True)
    response_id = Column(Integer, ForeignKey("questionnaire_responses.id", ondelete="CASCADE"))
    question_id = Column(Integer, ForeignKey("question_templates.id", ondelete="CASCADE"))
    selected_option_id = Column(Integer, ForeignKey("option_templates.id", ondelete="CASCADE"))

    response = relationship("QuestionnaireResponse", backref="answers")
    question = relationship("QuestionTemplate")
    selected_option = relationship("OptionTemplate")
