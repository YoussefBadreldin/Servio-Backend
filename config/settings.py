import os
from pathlib import Path
from pydantic import BaseSettings, AnyUrl

class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str = "Servio Backend"
    PROJECT_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", False)
    API_PREFIX: str = "/api/v1"
    
    # Data
    DATA_DIR: Path = Path(__file__).parent.parent / "data"
    SERVICE_REGISTRY_PATH: Path = DATA_DIR / "service_registry.json"
    SERVIO_DATA_PATH: Path = DATA_DIR / "servio_data.jsonl"
    
    # GitHub
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    GITHUB_SEARCH_LIMIT: int = 10
    
    # NLP
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    # LLM
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = "llama3-8b-8192"
    
    # Security
    API_KEY: str = os.getenv("API_KEY", "dev-key")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "secret-key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 week
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()