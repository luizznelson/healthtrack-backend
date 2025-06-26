from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum

# --- Enum de papéis ---
class RoleEnum(str, Enum):
    paciente = 'paciente'
    nutricionista = 'nutricionista'

# --- Auth ---
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    


class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str
    role: RoleEnum = RoleEnum.paciente
    nutricionista_id: Optional[int] = None

class User(UserBase):
    id: int
    role: RoleEnum

    model_config = {
        "from_attributes": True
    }

# --- Questionários estáticos (legado) ---
class QuestionarioBase(BaseModel):
    respostas: str

class QuestionarioCreate(QuestionarioBase):
    pass

class Questionario(QuestionarioBase):
    id: int
    data: datetime
    owner_id: int

    model_config = {
        "from_attributes": True
    }
    
class RelatorioCreate(BaseModel):
    paciente_id: int
    conteudo: str

# --- Relatório ---
class Relatorio(BaseModel):
    id: int
    conteudo: str
    paciente_id: int
    nutricionista_id: int
    data_criacao: datetime

    model_config = {
        "from_attributes": True
    }

# --- Questionários dinâmicos ---
class OptionTemplateBase(BaseModel):
    text: str
    score: int
    is_default: Optional[bool] = False

class OptionTemplateCreate(OptionTemplateBase):
    pass

class OptionTemplate(OptionTemplateBase):
    id: int

    model_config = {
        "from_attributes": True
    }

class QuestionTemplateBase(BaseModel):
    text: str
    order: int
    options: List[OptionTemplateCreate]

class QuestionTemplateCreate(QuestionTemplateBase):
    pass

class QuestionTemplate(QuestionTemplateBase):
    id: int
    options: List[OptionTemplate]

    model_config = {
        "from_attributes": True
    }

class QuestionnaireTemplateBase(BaseModel):
    title: str
    description: Optional[str] = None
    questions: List[QuestionTemplateCreate]

class QuestionnaireTemplateCreate(QuestionnaireTemplateBase):
    pass

class QuestionnaireTemplateOut(QuestionnaireTemplateBase):
    id: int
    questions: List[QuestionTemplate]

    model_config = {
        "from_attributes": True
    }

class Answer(BaseModel):
    question_id: int
    option_id: int

class QuestionnaireResponseIn(BaseModel):
    answers: List[Answer]

class QuestionnaireResponseOut(BaseModel):
    template_id: int
    total_score: int
    paciente_id: int
    interpretation: str
    data_resposta: datetime

    model_config = {
        "from_attributes": True
    }

