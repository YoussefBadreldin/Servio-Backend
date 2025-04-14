from pydantic import BaseModel
from typing import List, Optional, Dict

class Aspect(BaseModel):
    key: str
    value: str

class CreateXmlRequest(BaseModel):
    aspects: List[Aspect]

class DiscoveryRequest(BaseModel):
    query: str
    xml_path: str

class ServiceMatch(BaseModel):
    func_name: str
    repo: str
    path: str
    docstring: str
    url: str
    similarity_score: float

class DiscoveryResponse(BaseModel):
    matches: List[ServiceMatch]