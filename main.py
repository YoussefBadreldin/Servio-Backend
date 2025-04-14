# servio-backend/main.py
from fastapi import FastAPI
from app.modules.guided.routes import router as guided_router
from app.modules.direct.routes import router as direct_router
from app.modules.registry_builder.routes import router as registry_router

app = FastAPI()
app.include_router(guided_router)
app.include_router(direct_router)
app.include_router(registry_router)

@app.get("/")
def read_root():
    return {"message": "Servio API is running"}