from sqlalchemy.orm import Session
from app.models.barbeiro import Barbeiro
from app.schemas.barbeiro import BarbeiroCreate

def criar_barbeiro(db: Session, dados: BarbeiroCreate) -> Barbeiro:
    barbeiro = Barbeiro(
            nome=dados.nome, 
            telefone=dados.telefone
        )
    db.add(barbeiro)
    db.commit()
    db.refresh(barbeiro)
    return barbeiro

def buscar_barbeiro_por_id(db: Session, barbeiro_id: int) -> Barbeiro | None:
    barbeiro = db.get(Barbeiro, barbeiro_id)
    return barbeiro 
