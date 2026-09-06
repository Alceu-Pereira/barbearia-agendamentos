from fastapi import FastAPI
from app.routers.cliente import router as cliente_router

app = FastAPI()

app.include_router(cliente_router)

@app.get("/")
def health():
    return {
        "status": "Ok",
    }