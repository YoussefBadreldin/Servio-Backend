from fastapi import FastAPI, Query
from app.services.semantic_search import semantic_search
from app.services.syntactic_search import syntactic_search
from app.utils.file_utils import load_json
import os

app = FastAPI()

# Path to JSON file
DATA_FILE = "data/servio_data.json"

# Load service registry
service_registry = load_json(DATA_FILE)

# Semantic Search API
@app.get("/semantic-search")
def semantic_search_api(
    query: str = Query(..., description="Search query"),
    aspects: str = Query(default="docstring", description="Comma-separated aspects for semantic search"),
    top_n: int = Query(default=5, description="Number of top results to return")
):
    """
    API endpoint for semantic search.
    """
    aspects_list = [aspect.strip() for aspect in aspects.split(",")]
    results = semantic_search(query, service_registry, aspects_list, top_n)
    return {"results": results}

# Syntactic Search API
@app.get("/syntactic-search")
def syntactic_search_api(
    query: str = Query(..., description="Search query"),
    field: str = Query(default="func_name", description="Field for syntactic search"),
    top_n: int = Query(default=5, description="Number of top results to return")
):
    """
    API endpoint for syntactic search.
    """
    results = syntactic_search(query, service_registry, field, top_n)
    return {"results": results}