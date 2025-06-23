# servio-backend/app/modules/direct/models.py
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

class MCPDiscoveryRequest(BaseModel):
    user_requirements: dict

class MCPServiceMatch(BaseModel):
    rank: int
    service_name: str
    matched_features: list
    reason_for_match: str

class MCPDiscoveryResponse(BaseModel):
    matches: list[MCPServiceMatch]