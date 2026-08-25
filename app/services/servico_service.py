from sqlalchemy.orm import Session
from app.models.servico import Servico
from app.schemas.servico import ServicoCreate

def criar_servico(db: Session, dados: ServicoCreate) -> Servico:
    servico = Servico(
        nome=dados.nome,
        duracao_minutos=dados.duracao_minutos,
        preco=dados.preco
    )

    db.add(servico)
    db.commit()
    db.refresh(servico)

    return servico

def buscar_servico_por_id(db: Session, servico_id: int) -> Servico | None:
    servico = db.get(Servico, servico_id)
    return servico