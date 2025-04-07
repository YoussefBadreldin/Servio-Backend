from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.core import exceptions
from app.modules.direct.api import router as direct_router
from app.modules.guided.api import router as guided_router
from app.modules.registry.api import router as registry_router

# Initialize logging
from app.config.logging import configure_logging
configure_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(direct_router, prefix=settings.API_PREFIX + "/direct")
app.include_router(guided_router, prefix=settings.API_PREFIX + "/guided")
app.include_router(registry_router, prefix=settings.API_PREFIX + "/registry")

# Exception handlers
exceptions.include_exception_handlers(app)

@app.get("/")
async def root():
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "docs": "/docs",
        "status": "running"
    }