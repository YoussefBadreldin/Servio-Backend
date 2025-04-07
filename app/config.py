from pathlib import Path

class Settings:
    PROJECT_NAME = "Servio Backend"
    PROJECT_VERSION = "1.0.0"
    
    # Data paths
    DATA_DIR = Path(__file__).parent / "data"
    SERVICE_REGISTRY_PATH = DATA_DIR / "service_registry.json"
    SERVIO_DATA_PATH = DATA_DIR / "servio_data.jsonl"
    
    # GitHub API
    GITHUB_TOKEN = "your_github_token_here"  # Replace with environment variable in production
    
    # Vector Store
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    
settings = Settings()