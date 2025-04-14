from fastapi import APIRouter, UploadFile, File, HTTPException
from .models import (
    CreateXmlRequest,
    DiscoveryRequest,
    DiscoveryResponse,
    Aspect
)
from .service import DirectService
from ...shared.exceptions import DirectModuleError
import os
import uuid

router = APIRouter(
    prefix="/api/direct",
    tags=["direct"],
    responses={404: {"description": "Not found"}},
)

service = DirectService()

@router.get("/suggest-aspects")
async def get_suggestions():
    try:
        return {"suggested_aspects": service.suggest_aspects()}
    except DirectModuleError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create-xml")
async def create_xml(request: CreateXmlRequest):
    try:
        aspects = [{"key": a.key, "value": a.value} for a in request.aspects]
        xml_path = service.generate_xml(aspects)
        return {"xml_path": xml_path}
    except DirectModuleError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload-xml")
async def upload_xml(file: UploadFile = File(...)):
    try:
        # Save uploaded file
        xml_id = str(uuid.uuid4())
        xml_path = os.path.join(service.xml_storage_path, f"{xml_id}.xml")
        
        with open(xml_path, "wb") as f:
            f.write(await file.read())
        
        return {"xml_path": xml_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

@router.post("/discover", response_model=DiscoveryResponse)
async def discover_services(request: DiscoveryRequest):
    try:
        aspects = service.parse_xml(request.xml_path)
        matches = service.match_services(request.query, aspects)
        
        formatted_matches = []
        for match in matches:
            formatted_matches.append({
                "func_name": match.get("func_name", "Unknown"),
                "repo": match.get("repo", "Unknown"),
                "path": match.get("path", "Unknown"),
                "docstring": match.get("docstring", "No docstring available"),
                "url": match.get("url", "Unknown"),
                "similarity_score": match["similarity_score"]
            })
        
        return {"matches": formatted_matches}
    except DirectModuleError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="XML file not found")