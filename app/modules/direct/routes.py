from fastapi import APIRouter, Query, HTTPException
from typing import List, Dict, Any
from .models import (
    DirectDiscoveryRequest,
    DirectDiscoveryResponse,
    GenerateXmlRequest,
    DiscoveryMode
)
from .service import DirectService
from ...shared.exceptions import DirectMatchError

router = APIRouter(
    prefix="/api/direct",
    tags=["direct"],
    responses={404: {"description": "Not found"}},
)

direct_service = DirectService()

@router.post("/discover", response_model=DirectDiscoveryResponse)
async def discover_services(request: DirectDiscoveryRequest):
    try:
        aspects = []
        if request.xml_content:
            aspects = direct_service.parse_xml(request.xml_content)
        elif request.aspects:
            aspects = [a.dict() for a in request.aspects]
        else:
            raise DirectMatchError("Either xml_content or aspects must be provided")
            
        suggested_aspects = direct_service._suggest_missing_aspects(
            {a['key']: a['value'] for a in aspects}
        )
        
        # Run both modes if not specified
        run_parallel = request.mode == DiscoveryMode.PARALLEL or request.mode is None
        run_sequential = request.mode == DiscoveryMode.SEQUENTIAL or request.mode is None
        
        response = DirectDiscoveryResponse(suggested_aspects=suggested_aspects)
        
        if run_parallel:
            parallel_matches, parallel_time = direct_service.discover_services(
                request.query,
                aspects,
                DiscoveryMode.PARALLEL,
                request.top_n
            )
            response.parallel_results = {
                "query": request.query,
                "mode": "parallel",
                "matches": parallel_matches,
                "execution_time_ms": parallel_time
            }
            
        if run_sequential:
            sequential_matches, sequential_time = direct_service.discover_services(
                request.query,
                aspects,
                DiscoveryMode.SEQUENTIAL,
                request.top_n
            )
            response.sequential_results = {
                "query": request.query,
                "mode": "sequential",
                "matches": sequential_matches,
                "execution_time_ms": sequential_time
            }
            
        return response
    except DirectMatchError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Discovery failed: {str(e)}")

@router.post("/generate-xml", response_model=str)
async def generate_xml(request: GenerateXmlRequest):
    try:
        return direct_service.generate_xml([a.dict() for a in request.aspects])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"XML generation failed: {str(e)}")

@router.get("/latest-xml", response_model=str)
async def get_latest_xml():
    try:
        xml_content = direct_service.get_latest_xml()
        if not xml_content:
            raise HTTPException(status_code=404, detail="No XML files found")
        return xml_content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/suggest-aspects", response_model=List[str])
async def suggest_aspects(
    current_aspects: str = Query("", description="Comma-separated key:value pairs")
):
    try:
        aspects_dict = {}
        if current_aspects:
            for pair in current_aspects.split(','):
                if ':' in pair:
                    key, value = pair.split(':', 1)
                    aspects_dict[key.strip()] = value.strip()
        return direct_service._suggest_missing_aspects(aspects_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))