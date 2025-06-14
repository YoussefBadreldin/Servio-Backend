# servio-backend/app/modules/registry_builder/routes.py
from fastapi import APIRouter, HTTPException
from .models import GitHubSearchRequest, RegistryBuildResponse
from .service import RegistryBuilderService
from ...shared.exceptions import RegistryBuilderError
import os

router = APIRouter(
    prefix="/api/registry_builder",
    tags=["registry_builder"],
    responses={404: {"description": "Not found"}},
)

service = RegistryBuilderService()

@router.post("/build", response_model=RegistryBuildResponse)
async def build_registry(request: GitHubSearchRequest):
    try:
        result = service.build_registry(request.query, request.limit)
        if not result["success"]:
            raise RegistryBuilderError(result["message"])
        return result
    except RegistryBuilderError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/list_registries")
async def list_registries():
    try:
        registry_dir = "data/custom_registries"
        registries = [f for f in os.listdir(registry_dir) if f.endswith('.jsonl')]
        return {"registries": registries}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/suggestions")
async def get_registry_suggestions():
    try:
        return {
            "success": True,
            "registries": service.get_existing_registries()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    