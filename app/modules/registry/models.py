# app/modules/registry/models.py
from pydantic import BaseModel
from typing import List, Optional

class RepoInfo(BaseModel):
    name: str
    description: Optional[str] = None
    stars: int
    forks: int
    url: str

class RegistryResponse(BaseModel):
    repos: List[RepoInfo]
    count: int