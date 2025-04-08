# app/modules/registry/models.py
from pydantic import BaseModel
from typing import List, Optional

class RepoInfo(BaseModel):
    name: str
    full_name: str
    description: Optional[str]
    url: str
    stars: int
    forks: int
    language: Optional[str]
    license: Optional[str]
    readme_preview: str

class RegistryRequest(BaseModel):
    query: str
    limit: int = 10
    sort: str = "stars"
    order: str = "desc"

class RegistryResponse(BaseModel):
    query: str
    repos: List[RepoInfo]
    count: int
    from_cache: bool