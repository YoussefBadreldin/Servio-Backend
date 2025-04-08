# app/modules/direct/api.py
from fastapi import APIRouter, Depends, HTTPException
from app.core.dependencies import get_api_key
from app.core.exceptions import ServioException
from .models import DirectRequest, DirectResponse
from .service import DirectProcessor
from typing import List

router = APIRouter(
    dependencies=[Depends(get_api_key)],
    responses={404: {"description": "Not found"}},
)

processor = DirectProcessor()

@router.post("/process", response_model=DirectResponse)
async def process_direct(input: DirectRequest):
    try:
        result = processor.process(input)
        return DirectResponse(**result)
    except ServioException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/aspects", response_model=List[str])
async def get_available_aspects():
    return processor.get_available_aspects()