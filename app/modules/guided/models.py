from typing import List
from pydantic import BaseModel

class ServiceRecommendation(BaseModel):
    service_name: str
    confidence: float
    description: str
    url: str

class RecommendationResponse(BaseModel):
    explanation: str
    recommendations: List[ServiceRecommendation]

class UMLProcessingRequest(BaseModel):
    image_path: str

class UMLProcessingResponse(BaseModel):
    plantuml_code: str