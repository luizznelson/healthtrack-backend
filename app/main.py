from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, questionario, nutricionistas
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão dos routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(questionario.router, prefix="/questionarios", tags=["questionarios"])
app.include_router(nutricionistas.router, prefix="/nutricionistas", tags=["nutricionistas"])
