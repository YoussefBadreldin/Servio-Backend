# main.py - FastAPI entry point
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.modules.direct.api import router as direct_router
from app.modules.guided.api import router as guided_router
from app.modules.registry.api import router as registry_router
import nltk
import os

# Download NLTK data
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Servio Backend API - Complete Implementation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(direct_router, prefix="/api/direct", tags=["Direct Module"])
app.include_router(guided_router, prefix="/api/guided", tags=["Guided Module"])
app.include_router(registry_router, prefix="/api/registry", tags=["Registry Module"])

@app.on_event("startup")
async def startup_event():
    # Ensure data directory exists
    os.makedirs("app/data", exist_ok=True)
    
    # Initialize default registry if not exists
    if not os.path.exists("app/data/service_registry.json"):
        with open("app/data/service_registry.json", "w") as f:
            f.write("[]")

@app.get("/")
async def root():
    return {
        "message": "Servio Backend is running",
        "endpoints": {
            "direct": "/api/direct",
            "guided": "/api/guided",
            "registry": "/api/registry"
        }
    }