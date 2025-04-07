# main.py - FastAPI entry point
from fastapi import FastAPI
from app.core.config import settings
from app.modules.direct.api import router as direct_router
from app.modules.guided.api import router as guided_router
from app.modules.registry.api import router as registry_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Servio Backend API",
    version="1.0.0"
)

app.include_router(direct_router, prefix="/api/direct", tags=["direct"])
app.include_router(guided_router, prefix="/api/guided", tags=["guided"])
app.include_router(registry_router, prefix="/api/registry", tags=["registry"])

@app.get("/")
async def root():
    return {"message": "Servio Backend is running"}