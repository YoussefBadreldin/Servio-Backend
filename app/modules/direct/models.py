from pydantic import BaseModel
from typing import Optional, List, Dict, Union
from enum import Enum

class DiscoveryMode(str, Enum):
    PARALLEL = "parallel"
    SEQUENTIAL = "sequential"

class Aspect(BaseModel):
    key: str
    value: str

class GenerateXmlRequest(BaseModel):
    aspects: List[Aspect]

class DirectDiscoveryRequest(BaseModel):
    query: str
    mode: DiscoveryMode = DiscoveryMode.PARALLEL
    top_n: int = 5
    xml_content: Optional[str] = None  # For ready XML
    aspects: Optional[List[Aspect]] = None  # For generated aspects

class ServiceMatch(BaseModel):
    func_name: str
    repo: str
    path: str
    docstring: str
    url: str
    score: float
    matched_aspects: List[str]

class DiscoveryResult(BaseModel):
    query: str
    mode: str
    matches: List[ServiceMatch]
    execution_time_ms: float

class DirectDiscoveryResponse(BaseModel):
    parallel_results: Optional[DiscoveryResult] = None
    sequential_results: Optional[DiscoveryResult] = None
    suggested_aspects: List[str]