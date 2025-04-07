# app/modules/direct/models.py
from pydantic import BaseModel
from typing import Dict, List, Optional

class DirectRequest(BaseModel):
    query: str
    xml_option: int
    aspects: Dict[str, str]

class DirectResponse(BaseModel):
    matches: List[Dict]
    suggestions: List[str]
    status: str