from pydantic import BaseModel
from typing import Optional, Dict

class QueryRequest(BaseModel):
    query: str
    workflow: str = "guided"
    aspects: Optional[Dict[str, str]] = None
    registry: str = "servio_data.jsonl"

class ServiceRecommendation(BaseModel):
    service_name: str
    description: str
    confidence: float
    url: str