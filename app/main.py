from fastapi import FastAPI
from app.routers import auth, questionario, nutricionistas
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(questionario.router, prefix="/questionarios", tags=["questionarios"])
app.include_router(nutricionistas.router, prefix="/nutricionistas", tags=["nutricionistas"])