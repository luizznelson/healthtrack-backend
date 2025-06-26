from sqlalchemy.orm import Session
from app.models import User, Relatorio, UserRole 

def get_pacientes(db: Session, nutricionista_id: int):
    return db.query(User).filter(
        User.role == UserRole.paciente,
        User.nutricionista_id == nutricionista_id
    ).all()

def get_relatorios_por_paciente(db: Session, paciente_id: int):
    return db.query(Relatorio).filter(Relatorio.paciente_id == paciente_id).all()
