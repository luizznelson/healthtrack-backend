from enum import Enum as PyEnum
from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Text,
    Boolean, Enum as SqlEnum
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class UserRole(PyEnum):
    paciente = 'paciente'
    nutricionista = 'nutricionista'

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(SqlEnum(UserRole), default=UserRole.paciente)

    # --- Relação com questionários (legado) ---
    questionarios = relationship(
        'Questionario',
        back_populates='owner',
        foreign_keys='Questionario.owner_id',
        cascade='all, delete-orphan'
    )

    # --- Relações com relatórios ---
    relatorios_paciente = relationship(
        'Relatorio',
        back_populates='paciente',
        foreign_keys='Relatorio.paciente_id',
        cascade='all, delete-orphan'
    )
    relatorios_nutricionista = relationship(
        'Relatorio',
        back_populates='nutricionista',
        foreign_keys='Relatorio.nutricionista_id',
        cascade='all, delete-orphan'
    )

class Questionario(Base):
    __tablename__ = 'questionarios'
    id = Column(Integer, primary_key=True, index=True)
    respostas = Column(Text)          # conforme seu schema legado
    data = Column(DateTime, default=datetime.utcnow)
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
    data_criacao = Column(DateTime, default=datetime.utcnow)

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