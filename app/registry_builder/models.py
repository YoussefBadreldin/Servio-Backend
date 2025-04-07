from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class GitHubRepository(BaseModel):
    name: str
    full_name: str
    description: Optional[str]
    url: str
    stars: int
    forks: int
    language: Optional[str]
    license: Optional[str]
    readme: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    topics: List[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)

class RegistryBuildRequest(BaseModel):
    search_query: str
    max_results: int = 10
    output_path: str = "service_registry.json"
    format: str = "json"  # json or jsonl

class RegistryBuildResponse(BaseModel):
    status: str
    repository_count: int
    output_path: str
    search_query: str
    timestamp: str