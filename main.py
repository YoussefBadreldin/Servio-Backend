# servio-backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.modules.guided.routes import router as guided_router
from app.modules.direct.routes import router as direct_router
from app.modules.registry_builder.routes import router as registry_router
import os

app = FastAPI()

# Get allowed origins from environment variable or use default
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(guided_router)
app.include_router(direct_router)
app.include_router(registry_router)

@app.get("/")
def read_root():
    return {"message": "Servio API is running"}