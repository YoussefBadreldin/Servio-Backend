from fastapi import APIRouter, UploadFile, File, Depends
from .service import GuidedDiscoveryService
from .models import SearchQuery, ServiceRecommendation, UploadResponse
from app.core.dependencies import SecurityDep

router = APIRouter()
service = GuidedDiscoveryService()

@router.post("/recommend", response_model=tuple[str, list[ServiceRecommendation]])
async def recommend_services(
    query: SearchQuery,
    api_key: SecurityDep
):
    return await service.recommend_services(query)

@router.post("/upload", response_model=UploadResponse)
async def upload_registry(
    file: UploadFile = File(...),
    api_key: SecurityDep = Depends()
):
    success = await service.process_upload(file)
    return UploadResponse(
        success=success,
        message="Registry processed successfully" if success else "Processing failed"
    )