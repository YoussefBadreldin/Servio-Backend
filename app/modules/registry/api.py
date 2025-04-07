# app/modules/registry/api.py
from fastapi import APIRouter, Depends
from app.core.dependencies import get_query_token
from .models import RegistryResponse
from .service import fetch_repositories

router = APIRouter(
    prefix="/registry",
    tags=["registry"],
    dependencies=[Depends(get_query_token)]
)

@router.get("/fetch", response_model=RegistryResponse)
async def fetch_repos(query: str, limit: int = 10):
    return fetch_repositories(query, limit)