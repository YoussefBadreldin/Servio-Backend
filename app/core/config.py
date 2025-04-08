# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Servio Backend"
    API_V1_STR: str = "/api/v1"
    GITHUB_TOKEN: str = ""
    GROQ_API_KEY: str = ""
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True

settings = Settings()