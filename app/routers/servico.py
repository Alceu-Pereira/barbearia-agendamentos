from fastapi import APIRouter, HTTPException, Depends

from app.database import get_db
from sqlalchemy.orm import Session

from app.services.servico_service import criar_servico, buscar_servico_por_id

from app.schemas.servico import ServicoCreate, ServicoResponse

router = APIRouter(
    prefix="/api/v1/servicos",
    tags=["servico"],
)

@router.post("/", response_model=ServicoResponse)
def criar_servico_router(dados: ServicoCreate, db: Session = Depends(get_db)):
    return criar_servico(db, dados)

@router.get("/{servico_id}", response_model=ServicoResponse)
def buscar_servico_por_id_router(servico_id: int, db: Session = Depends(get_db)):
    servico = buscar_servico_por_id(db, servico_id)
    if servico is None:
        raise HTTPException(status_code=404, detail="Serviço não encontrado.")
    return servico