from sqlalchemy.orm import Session
from app.models import User, Relatorio

def get_pacientes(db: Session, nutricionista_id: int):
    return db.query(User).filter(User.role=='paciente').all()

def get_relatorios_por_paciente(db: Session, paciente_id: int):
    return db.query(Relatorio).filter(Relatorio.paciente_id == paciente_id).all()