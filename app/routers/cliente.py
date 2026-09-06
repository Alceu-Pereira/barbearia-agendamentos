from fastapi import APIRouter, HTTPException

from app.services.cliente_service import criar_cliente, buscar_cliente_por_id

from sqlalchemy.orm import Session
from app.database import get_db
from fastapi import Depends

from app.schemas.cliente import ClienteCreate, ClienteResponse

router = APIRouter(
    prefix="/api/v1/clientes",
    tags=["cliente"]
)

@router.post("/", response_model=ClienteResponse)
def criar_cliente_router(dados: ClienteCreate, db: Session = Depends(get_db)):
    return criar_cliente(db, dados)

@router.get("/{cliente_id}", response_model=ClienteResponse)
def buscar_cliente_router(cliente_id: int, db: Session = Depends(get_db)):
    cliente = buscar_cliente_por_id(db, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente