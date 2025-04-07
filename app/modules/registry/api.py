from fastapi import APIRouter, Depends
from .service import RegistryService
from .models import GitHubSearchParams, Repository
from app.core.dependencies import SecurityDep

router = APIRouter()
service = RegistryService()

@router.post("/search", response_model=list[Repository])
async def search_github(
    params: GitHubSearchParams,
    api_key: SecurityDep
):
    return await service.fetch_repositories(params)

@router.get("/local", response_model=list[Repository])
async def get_local_registry(api_key: SecurityDep):
    return await service.get_registry()