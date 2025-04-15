# servio-backend/app/modules/registry_builder/models.py
from pydantic import BaseModel
from typing import Optional, List

class GitHubSearchRequest(BaseModel):
    query: str
    limit: Optional[int] = 5

class RepositoryInfo(BaseModel):
    func_name: str
    full_name: str
    docstring: Optional[str]
    url: str
    stars: int
    forks: int
    language: Optional[str]
    license: Optional[str]
    readme: Optional[str]

class RegistryBuildResponse(BaseModel):
    success: bool
    message: str
    registry_path: str  # Changed from filename to registry_path
    repositories: Optional[List[RepositoryInfo]]