from fastapi import APIRouter, Depends
from .service import DirectDiscoveryService
from .models import SearchRequest, AspectMatchRequest, ServiceMatch
from app.core.dependencies import SecurityDep

router = APIRouter()
service = DirectDiscoveryService()

@router.post("/search", response_model=list[ServiceMatch])
async def search_services(
    request: SearchRequest,
    api_key: SecurityDep
):
    return await service.search_services(request)

@router.post("/match-aspect", response_model=list[ServiceMatch])
async def match_aspect(
    request: AspectMatchRequest,
    api_key: SecurityDep
):
    return await service.match_aspect(request)