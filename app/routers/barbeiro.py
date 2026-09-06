from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.orm import Session

from app.services.barbeiro_service import criar_barbeiro, buscar_barbeiro_por_id

from app.schemas.barbeiro import BarbeiroCreate, BarbeiroResponse

from app.database import get_db

router = APIRouter(
    prefix="/api/v1/barbeiros",
    tags=["barbeiro"],
)

@router.post("/", response_model=BarbeiroResponse)
def criar_barbeiro_router(dados: BarbeiroCreate, db: Session = Depends(get_db)):
    return criar_barbeiro(db, dados)

@router.get("/{barbeiro_id}", response_model=BarbeiroResponse)
def buscar_barbeiro_por_id_router(barbeiro_id: int, db: Session = Depends(get_db)):
    barbeiro = buscar_barbeiro_por_id(db, barbeiro_id)
    if barbeiro is None:
        raise HTTPException(status_code=404, detail="Barbeiro não encontrado.")
    return barbeiro