from sqlalchemy.orm import Session
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate

def criar_cliente(db: Session, dados: ClienteCreate) -> Cliente:
    cliente = Cliente(
            nome=dados.nome, 
            telefone=dados.telefone
        )
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente

def buscar_cliente_por_id(db: Session, cliente_id: int) -> Cliente | None:
    cliente = db.get(Cliente, cliente_id)
    return cliente