from pydantic import BaseModel
from typing import Dict, Optional, List

class AspectMatchRequest(BaseModel):
    aspect_key: str
    aspect_value: str
    min_threshold: float = 0.3
    top_n: int = 3

class SearchRequest(BaseModel):
    query: str
    aspects: Dict[str, str]
    min_threshold: float = 0.3
    top_n: int = 5
    required_matches: int = 1

class ServiceMatch(BaseModel):
    func_name: str
    repo: str
    path: str
    docstring: str
    url: str
    score: float