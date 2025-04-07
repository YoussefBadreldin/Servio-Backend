# app/modules/guided/api.py
from pydantic import BaseModel

class GuidedRequest(BaseModel):
    query: str
    format: str  # 'json' or 'xml'

class GuidedResponse(BaseModel):
    results: list
    format: str
    status: str