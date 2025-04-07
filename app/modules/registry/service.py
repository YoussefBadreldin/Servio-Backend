# app/modules/registry/service.py
import json
from pathlib import Path
from .models import RegistryResponse, RepoInfo
from app.core.exceptions import ServioException

def fetch_repositories(query: str, limit: int) -> RegistryResponse:
    try:
        # This would actually call GitHub API in real implementation
        # For now using your JSON file approach
        data_path = Path("app/data/service_registry.json")
        if not data_path.exists():
            raise ServioException("Registry data not found")
            
        with open(data_path) as f:
            data = json.load(f)
            
        repos = [
            RepoInfo(
                name=repo.get("name", ""),
                description=repo.get("description"),
                stars=repo.get("stars", 0),
                forks=repo.get("forks", 0),
                url=repo.get("url", "")
            ) for repo in data[:limit]
        ]
        
        return RegistryResponse(repos=repos, count=len(repos))
        
    except Exception as e:
        raise ServioException(str(e))