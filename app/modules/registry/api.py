# app/modules/registry/api.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi import BackgroundTasks
from app.core.dependencies import get_api_key
from app.core.exceptions import ServioException
from .models import RegistryRequest, RegistryResponse, RepoInfo
from .service import RegistryService

router = APIRouter(
    dependencies=[Depends(get_api_key)],
    responses={404: {"description": "Not found"}},
)

service = RegistryService()

@router.get("/fetch", response_model=RegistryResponse)
async def fetch_repos(query: str, limit: int = 10):
    try:
        return service.fetch_from_cache(query, limit)
    except ServioException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/refresh", status_code=202)
async def refresh_registry(background_tasks: BackgroundTasks):
    background_tasks.add_task(service.refresh_registry)
    return {"message": "Registry refresh started in background"}