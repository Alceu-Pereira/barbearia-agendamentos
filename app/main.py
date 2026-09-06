from fastapi import FastAPI

from app.routers.cliente import router as cliente_router
from app.routers.barbeiro import router as barbeiro_router
from app.routers.servico import router as servico_router

app = FastAPI()

app.include_router(cliente_router)
app.include_router(barbeiro_router)
app.include_router(servico_router)

@app.get("/")
def health():
    return {
        "status": "Ok",
    }