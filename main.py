from fastapi import FastAPI
from app.modules.guided.routes import router as guided_router

app = FastAPI()
app.include_router(guided_router)

@app.get("/")
def read_root():
    return {"message": "Servio API is running"}