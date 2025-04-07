from fastapi import FastAPI
from app.routes.api import router as api_router
from app.routes.direct import router as direct_router
from app.routes.guided import router as guided_router
from app.routes.registry import router as registry_router

app = FastAPI(title="Servio Backend API")

# Include routers
app.include_router(api_router, prefix="/api", tags=["api"])
app.include_router(direct_router, prefix="/direct", tags=["direct"])
app.include_router(guided_router, prefix="/guided", tags=["guided"])
app.include_router(registry_router, prefix="/registry", tags=["registry"])

@app.get("/")
async def root():
    return {"message": "Servio Backend API is running"}