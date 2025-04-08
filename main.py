# SERVIO-BACKEND/main.py
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict
import os
import json
import time
from dotenv import load_dotenv

# Load modules
from app.guided.query import recommend_services as guided_recommend
from app.guided.vectorizer import RegistryVectorizer
from app.direct.matching import DirectMatcher
from app.direct.xml_utils import AspectHandler
from app.direct.registry import RegistryLoader
from app.registry_builder.github_api import GitHubRegistryBuilder
from app.registry_builder.transformers import RegistryTransformer
from app.cache import cache
from app.utils import ensure_dirs

app = FastAPI()
load_dotenv()
ensure_dirs()
vectorizer = RegistryVectorizer()

# Models
class QueryRequest(BaseModel):
    query: str
    workflow: str = "guided"
    aspects: Optional[Dict[str, str]] = None
    registry: str = "servio_data.jsonl"
    top_n: Optional[int] = 5

class BuildRegistryRequest(BaseModel):
    query: Optional[str] = None
    limit: int = 10
    min_stars: int = 10
    format: str = "jsonl"

# Core Endpoints
@app.post("/query")
async def handle_query(request: QueryRequest):
    cache_key = f"{request.workflow}:{request.query}:{request.registry}"
    if cached := cache.get(cache_key):
        return JSONResponse(cached)
    
    registry_path = (
        f"{os.getenv('UPLOAD_DIR')}/{request.registry}"
        if request.registry != "servio_data.jsonl"
        else "./data/servio_data.jsonl"
    )
    
    if request.workflow == "guided":
        vector_store_path = vectorizer.vectorize_registry(registry_path)
        result = guided_recommend(request.query, vector_store_path)
    elif request.workflow == "direct":
        if not request.aspects:
            raise HTTPException(400, detail="Aspects required for DIRECT workflow")
        registry = RegistryLoader.load(registry_path)
        matcher = DirectMatcher()
        result = {
            "matches": matcher.match_services(
                request.query, 
                registry, 
                request.aspects,
                request.top_n or 5
            ),
            "suggested_aspects": RegistryLoader.suggest_aspects(request.aspects)
        }
    else:
        raise HTTPException(400, detail="Invalid workflow")
    
    cache.set(cache_key, result)
    return JSONResponse(result)

# Registry Management
@app.post("/registry/build")
async def build_registry(request: BuildRegistryRequest):
    """Build a registry from GitHub repositories"""
    builder = GitHubRegistryBuilder()
    transformer = RegistryTransformer()
    
    repos = builder.fetch_repositories(
        query=request.query,
        limit=request.limit,
        min_stars=request.min_stars
    )
    
    if request.format == "servio":
        repos = transformer.to_servio_format(repos)
    
    registry_path = f"{os.getenv('UPLOAD_DIR')}/registry_{int(time.time())}.jsonl"
    transformer.to_jsonl(repos, registry_path)
    
    return {
        "registry_path": registry_path,
        "repositories_found": len(repos),
        "sample_entry": repos[0] if repos else None
    }

@app.post("/upload/registry/{registry_name}")
async def upload_registry(registry_name: str, file: UploadFile):
    """Upload a custom registry file"""
    file_path = f"{os.getenv('UPLOAD_DIR')}/{registry_name}"
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    return {"message": f"Registry {registry_name} uploaded"}

# Aspect Management
@app.post("/aspects/upload")
async def upload_aspects(file: UploadFile):
    """Upload XML aspects file"""
    aspects_path = f"{os.getenv('UPLOAD_DIR')}/aspects_{int(time.time())}.xml"
    with open(aspects_path, "wb") as f:
        f.write(file.file.read())
    return {"path": aspects_path}

@app.post("/aspects/generate")
async def generate_aspects(aspects: Dict[str, str]):
    """Generate XML from aspects dictionary"""
    aspects_path = f"{os.getenv('UPLOAD_DIR')}/aspects_{int(time.time())}.xml"
    AspectHandler.generate_xml(aspects, aspects_path)
    return {"path": aspects_path}

# UML Processing
@app.post("/process/uml")
async def process_uml(file: UploadFile):
    """Process UML diagram to text"""
    file_path = f"{os.getenv('UPLOAD_DIR')}/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    
    # Process UML (would integrate with actual UML processor)
    return {"message": "UML processing would be implemented here"}

@app.get("/")
async def root():
    return {"message": "API is running"}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)