from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    # Define all your environment variables as fields
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str 
    POSTGRES_DB: str
    POSTGRES_HOST: str = "healthtrack-backend-db-1"
    POSTGRES_PORT: int = 5432
    
    @field_validator("ACCESS_TOKEN_EXPIRE_MINUTES", mode="before")
    def validate_token_expire_minutes(cls, v):
        return int(v) if isinstance(v, str) else v
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "allow"
    }

settings = Settings()