from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base
<<<<<<< Updated upstream
=======
from sqlalchemy.orm import relationship
>>>>>>> Stashed changes

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "patient" ou "nutritionist"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
<<<<<<< Updated upstream
=======
    questionarios = relationship("Questionario", back_populates="paciente", cascade="all, delete-orphan")
>>>>>>> Stashed changes
