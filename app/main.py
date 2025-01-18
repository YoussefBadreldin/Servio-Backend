from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import List, Optional
from app.services.semantic_search import semantic_search
from app.services.syntactic_search import syntactic_search
from app.utils.file_utils import load_json

app = FastAPI()

# Path to JSON file
DATA_FILE = "data/servio_data.json"

# Load service registry
service_registry = load_json(DATA_FILE)

# Define request models
class SemanticSearchRequest(BaseModel):
    query: str
    aspects: List[str] = ["docstring"]
    top_n: int = 5

class SyntacticSearchRequest(BaseModel):
    query: str
    field: str = "func_name"
    top_n: int = 5

# Combined Search API
@app.post("/search")
def search_api(
    search_type: str = Body(..., description="Type of search: 'semantic' or 'syntactic'"),
    semantic_request: Optional[SemanticSearchRequest] = Body(None),
    syntactic_request: Optional[SyntacticSearchRequest] = Body(None)
):
    """
    API endpoint for combined semantic and syntactic search.
    """
    if search_type == "semantic" and semantic_request:
        results = semantic_search(
            semantic_request.query,
            service_registry,
            semantic_request.aspects,
            semantic_request.top_n
        )
    elif search_type == "syntactic" and syntactic_request:
        results = syntactic_search(
            syntactic_request.query,
            service_registry,
            syntactic_request.field,
            syntactic_request.top_n
        )
    else:
        return {"error": "Invalid search type or missing request body."}

    # Format results to match the old code
    formatted_results = []
    for result in results:
        formatted_results.append({
            "function_name": result.get("func_name", "Unknown"),
            "url": result.get("url", "Unknown"),
            "docstring": result.get("docstring", "No docstring available")
        })

    return {"results": formatted_results}