from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

class ServiceRecommendation(BaseModel):
    service_name: str
    confidence: float
    description: str
    url: str

class RecommendationResponse(BaseModel):
    response_text: str
    recommendations: list[ServiceRecommendation]