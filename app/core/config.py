# servio-backend/app/core/config.py
from pydantic_settings import BaseSettings
from pydantic import Field, AnyHttpUrl  
from typing import List, Union

class Settings(BaseSettings):
    GROQ_API_KEY: str = Field(..., env="GROQ_API_KEY")
    DEBUG: bool = Field(False, env="DEBUG")
    FAISS_INDEX_PATH: str = Field("data/faiss_index", env="FAISS_INDEX_PATH")
    EMBEDDING_MODEL: str = Field("all-MiniLM-L6-v2", env="EMBEDDING_MODEL")
    CORS_ORIGINS: List[Union[str, AnyHttpUrl]] = Field(["*"], env="CORS_ORIGINS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()