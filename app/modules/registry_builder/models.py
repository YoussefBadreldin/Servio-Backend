# servio-backend/app/modules/registry_builder/models.py
from pydantic import BaseModel
from typing import Optional

class GitHubSearchRequest(BaseModel):
    query: str
    limit: Optional[int] = 10

class RepositoryInfo(BaseModel):
    name: str
    full_name: str
    description: Optional[str]
    url: str
    stars: int
    forks: int
    language: Optional[str]
    license: Optional[str]
    readme: Optional[str]

class RegistryBuildResponse(BaseModel):
    success: bool
    message: str
    filename: Optional[str]
    repositories: Optional[list[RepositoryInfo]]