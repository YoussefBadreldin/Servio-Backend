# app/modules/direct/api.py
from fastapi import APIRouter, Depends
from app.core.dependencies import get_query_token
from .models import DirectRequest, DirectResponse
from .service import process_direct_request

router = APIRouter(
    dependencies=[Depends(get_query_token)]
)

@router.post("/process", response_model=DirectResponse)
async def process_direct(input: DirectRequest):
    return process_direct_request(input)