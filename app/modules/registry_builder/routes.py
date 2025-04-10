from fastapi import APIRouter, HTTPException
from .models import ServiceData, BuildResponse
from .service import RegistryBuilderService

router = APIRouter()
service = RegistryBuilderService()

@router.post("/add-service")
async def add_service(service_data: ServiceData):
    try:
        return await service.add_service(service_data.dict())
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.post("/rebuild")
async def rebuild_registry():
    try:
        result = await service.rebuild_registry()
        return BuildResponse(
            status="success",
            new_services=0,
            total_services=0
        )
    except Exception as e:
        raise HTTPException(
            status_code=501,
            detail="Registry rebuild not implemented yet"
        )