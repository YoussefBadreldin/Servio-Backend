from pydantic import BaseModel
from typing import List, Optional

class GitHubSearchParams(BaseModel):
    query: str = "microservice language:python"
    sort: str = "stars"
    order: str = "desc"
    limit: int = 10

class Repository(BaseModel):
    name: str
    full_name: str
    description: Optional[str]
    url: str
    stars: int
    forks: int
    language: Optional[str]
    license: str
    readme: str