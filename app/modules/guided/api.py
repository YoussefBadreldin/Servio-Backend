# app/modules/guided/api.py
from fastapi import APIRouter, Depends
from app.core.dependencies import get_query_token
from .models import GuidedRequest, GuidedResponse
from .service import process_guided_request

router = APIRouter(
    dependencies=[Depends(get_query_token)]
)

@router.post("/process", response_model=GuidedResponse)
async def process_guided(input: GuidedRequest):
    return process_guided_request(input)