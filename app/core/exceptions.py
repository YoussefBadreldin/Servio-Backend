from typing import List, Dict, Optional
from pydantic import BaseModel

class AspectDefinition(BaseModel):
    key: str
    value: str

class ServiceMatch(BaseModel):
    func_name: str
    repo: str
    path: str
    docstring: str
    url: str
    score: float

class AspectMatchResult(BaseModel):
    aspect_key: str
    aspect_value: str
    matches: List[ServiceMatch]
    min_threshold: float

class OverallMatchResult(BaseModel):
    query: str
    matches: List[ServiceMatch]
    aspects_used: List[str]
    min_threshold: float

class XmlGenerationRequest(BaseModel):
    aspects: List[AspectDefinition]
    output_path: Optional[str] = "generated_aspects.xml"