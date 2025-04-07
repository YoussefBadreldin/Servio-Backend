from pydantic import BaseModel
from typing import List, Optional

class SearchQuery(BaseModel):
    query: str
    expand_query: bool = True

class ServiceRecommendation(BaseModel):
    service_name: str
    confidence: float
    description: str
    url: str

class UploadResponse(BaseModel):
    success: bool
    message: str
    records_processed: Optional[int] = None