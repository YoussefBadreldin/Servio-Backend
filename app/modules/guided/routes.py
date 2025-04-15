# servio-backend/app/modules/guided/routes.py
from fastapi import APIRouter, HTTPException
from .models import QueryRequest, RecommendationResponse, ServiceRecommendation
from .service import GuidedService
from ...shared.exceptions import ServiceDiscoveryError
from pathlib import Path
router = APIRouter(
    prefix="/api/guided",
    tags=["guided"],
    responses={404: {"description": "Not found"}},
)

service = GuidedService()

@router.post("/recommend", response_model=RecommendationResponse)
async def recommend_services(request: QueryRequest):
    try:
        result = service.recommend_services(request.query)
        return {
            "response_text": result["response_text"],
            "recommendations": [
                ServiceRecommendation(**rec) for rec in result["recommendations"]
            ]
        }
    except ServiceDiscoveryError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@router.post("/test")
async def test_endpoint(request: QueryRequest):
    """
    Test endpoint that mimics the original notebook test, but allows user-provided query.
    """
    try:
        user_query = request.query
        result = service.recommend_services(user_query)

        # Logging like in notebook
        print("Assistant Response:\n", result["response_text"])
        print("\nTop 5 Service Recommendations:")
        for rec in result["recommendations"]:
            print("-", rec)

        return {
            "response_text": result["response_text"],
            "recommendations": result["recommendations"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# servio-backend/app/modules/guided/routes.py
@router.post("/set-registry")
async def set_registry_path(request: dict):
    try:
        if request.get("use_default", False):
            service.reset_to_default()
        else:
            service.set_registry_path(request["registry_path"])
        return {
            "success": True,
            "message": "Registry path updated successfully",
            "registry_path": service.registry_path
        }
    except ServiceDiscoveryError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update registry: {str(e)}")