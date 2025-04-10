from pydantic import BaseModel
from typing import Dict, List

class ServiceData(BaseModel):
    func_name: str
    docstring: str
    repo: List[str]
    url: str
    metadata: Dict = {}

class BuildResponse(BaseModel):
    status: str
    new_services: int
    total_services: int