from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers.auth import router as auth_router
from app.routers.questionario import router as questionario_router

# cria tabelas automaticamente (em produção, use Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="HealthTrack API", debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(questionario_router)