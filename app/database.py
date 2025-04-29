# app/database.py
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Tenta conectar até 10 vezes, dormindo 2s entre as tentativas
for i in range(10):
    try:
        engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
        # Testa a conexão
        conn = engine.connect()
        conn.close()
        print("Conectou no Postgres após", i+1, "tentativa(s)")
        break
    except Exception as e:
        print(f"Postgres não disponível ({i+1}/10): {e}")
        time.sleep(2)
else:
    raise RuntimeError("Não foi possível conectar ao Postgres após várias tentativas")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
