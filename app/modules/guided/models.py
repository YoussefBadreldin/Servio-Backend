# app/modules/guided/models.py
from pydantic import BaseModel
from typing import List, Dict, Literal

FormatType = Literal['json', 'xml']

class GuidedRequest(BaseModel):
    query: str
    format: FormatType = 'json'
    expand_query: bool = True
    top_n: int = 5

class GuidedResponse(BaseModel):
    query: str
    expanded_query: str
    results: List[Dict]
    format: FormatType
    suggestions: List[str]