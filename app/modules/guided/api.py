# app/modules/guided/api.py
from fastapi import APIRouter, Depends, HTTPException
from app.core.dependencies import get_api_key
from app.core.exceptions import ServioException
from .models import GuidedRequest, GuidedResponse
from .service import GuidedProcessor

router = APIRouter(
    dependencies=[Depends(get_api_key)],
    responses={404: {"description": "Not found"}},
)

processor = GuidedProcessor()

@router.post("/process", response_model=GuidedResponse)
async def process_guided(input: GuidedRequest):
    try:
        result = processor.process(input)
        return GuidedResponse(**result)
    except ServioException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)