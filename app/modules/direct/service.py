# app/modules/direct/service.py
from app.modules.direct.models import DirectRequest, DirectResponse
from app.utils.nlp_utils import enhanced_similarity
from app.utils.file_handlers import load_registry

def process_direct_request(request: DirectRequest) -> DirectResponse:
    """Process direct request with enhanced similarity matching"""
    registry = load_registry("app/data/service_registry.json")
    
    # Implement your matching logic here
    matches = []
    for aspect_key, aspect_value in request.aspects.items():
        # Your matching logic from DIRECT_parallel.ipynb
        pass
    
    return DirectResponse(
        matches=matches,
        suggestions=[],
        status="success"
    )