# SERVIO-BACKEND/app/registry_builder/models.py
from typing import Optional

def fetch_readme(repo, max_length: int = 500) -> str:
    """Fetch and truncate README content"""
    try:
        content = repo.get_readme().decoded_content.decode("utf-8")
        return content[:max_length]
    except Exception:
        return "No README available"