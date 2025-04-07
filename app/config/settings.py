# app/config/settings.py
from app.core.config import settings

# Database settings (example)
DATABASE_URL = "sqlite:///./servio.db"

# Security settings
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30