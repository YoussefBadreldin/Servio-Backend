# app/modules/direct/models.py
from pydantic import BaseModel
from typing import Dict, List

class AspectMatch(BaseModel):
    aspect: str
    value: str
    score: float
    matched_services: List[Dict]

class DirectRequest(BaseModel):
    query: str
    aspects: Dict[str, str]
    min_threshold: float = 0.3
    top_n: int = 5

class DirectResponse(BaseModel):
    query: str
    overall_matches: List[Dict]
    aspect_matches: List[AspectMatch]
    suggested_aspects: List[str]