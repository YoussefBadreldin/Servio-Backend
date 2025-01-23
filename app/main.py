from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from app.services.semantic_search import semantic_search
from app.services.syntactic_search import syntactic_search
from app.utils.file_utils import load_json
import json
import torch
import nltk
nltk.download("wordnet")
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import wordnet

app = FastAPI()

# Add CORS middleware to handle preflight requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with allowed origins
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

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

class GuideSearchRequest(BaseModel):
    service_type: str
    features: str
    refinement: Optional[str] = None

# Function to load the model
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    return tokenizer, model

def expand_query(query):
    words = query.split()
    expanded_query = set(words)
    for word in words:
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                expanded_query.add(lemma.name().replace("_", " "))
    return " ".join(expanded_query)

def embed_text(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)

def retrieve_service(query, service_registry, tokenizer, model):
    expanded_query = expand_query(query)
    query_embedding = embed_text(expanded_query, tokenizer, model)
    registry_embeddings = [
        embed_text(service.get("docstring", ""), tokenizer, model)
        for service in service_registry
    ]
    similarities = [cosine_similarity(query_embedding, emb)[0][0] for emb in registry_embeddings]
    best_match_idx = similarities.index(max(similarities))
    best_service = service_registry[best_match_idx]

    func_name = best_service.get("func_name", "Unknown")
    url = best_service.get("url", "Unknown")
    docstring = best_service.get("docstring", "No description available.")
    return func_name, url, docstring

# Combined Search API for POST and OPTIONS
@app.api_route("/search", methods=["POST", "OPTIONS"])
def search_api(
    search_type: str = Body(..., description="Type of search: 'semantic', 'syntactic', or 'guide'"),
    semantic_request: Optional[SemanticSearchRequest] = Body(None),
    syntactic_request: Optional[SyntacticSearchRequest] = Body(None),
    guide_request: Optional[GuideSearchRequest] = Body(None),
):
    if search_type == "semantic" and semantic_request:
        results = semantic_search(
            semantic_request.query,
            service_registry,
            semantic_request.aspects,
            semantic_request.top_n,
        )
    elif search_type == "syntactic" and syntactic_request:
        results = syntactic_search(
            syntactic_request.query,
            service_registry,
            syntactic_request.field,
            syntactic_request.top_n
        )
    elif search_type == "guide" and guide_request:
        tokenizer, model = load_model()
        query = f"Service type: {guide_request.service_type}, Features: {guide_request.features}"
        if guide_request.refinement:
            query += f", {guide_request.refinement}"
        func_name, url, docstring = retrieve_service(query, service_registry, tokenizer, model)
        results = [
            {
                "function_name": func_name,
                "url": url,
                "docstring": docstring,
            }
        ]
    else:
        return {"error": "Invalid search type or missing request body."}

    formatted_results = []
    for result in results:
        formatted_results.append(
            {
                "function_name": result.get("function_name", result.get("func_name", "Unknown")),  # Check both keys
                "url": result.get("url", "Unknown"),
                "docstring": result.get("docstring", "No docstring available"),
            }
        )

    return {"results": formatted_results}

@app.options("/search")
def options_handler():
    """
    Handle OPTIONS request for preflight.
    """
    return JSONResponse(
        status_code=200,
        content={
            "methods": ["POST", "OPTIONS"],
            "message": "This endpoint supports POST and OPTIONS methods."
        }
    )
