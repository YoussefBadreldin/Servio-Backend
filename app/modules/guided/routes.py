# servio-backend/app/modules/guided/routes.py
from fastapi import APIRouter, HTTPException
from .models import QueryRequest, RecommendationResponse, ServiceRecommendation
from .service import GuidedService
from ...shared.exceptions import ServiceDiscoveryError

router = APIRouter(
    prefix="/api/guided",
    tags=["guided"],
    responses={404: {"description": "Not found"}},
)

guided_service = GuidedService()

@router.post("/recommend", response_model=RecommendationResponse)
async def recommend_services(request: QueryRequest):
    try:
        result = guided_service.recommend_services(request.query)
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
        result = guided_service.recommend_services(user_query)

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
