from fastapi import APIRouter, HTTPException, Depends

from app.schemas.agendamento import AgendamentoCreate, AgendamentoResponse

from app.services.agendamento_service import criar_agendamento, listar_disponibilidade, cancelar_agendamento

from app.services.exceptions import RecursoNaoEncontrado, ConflitoDeHorario, OperacaoInvalida

from sqlalchemy.orm import Session
from app.database import get_db
from datetime import date, datetime

router = APIRouter(
    prefix="/api/v1/agendamentos",
    tags=["agendamento"],
)

@router.post("/", response_model=AgendamentoResponse)
def criar_agendamento_router(dados: AgendamentoCreate, db: Session = Depends(get_db)):
    try:
        agendamento = criar_agendamento(db, dados)
    except RecursoNaoEncontrado:
        raise HTTPException(status_code=404, detail="Recurso não encontrado")
    except ConflitoDeHorario:
        raise HTTPException(status_code=409, detail="Conflito de horário")

    return agendamento

@router.get("/disponibilidade", response_model=list[datetime])
def listar_disponibilidade_router(barbeiro_id: int, data: date, db: Session = Depends(get_db)):
    try:
        horarios_disponiveis = listar_disponibilidade(db, barbeiro_id, data)
    except RecursoNaoEncontrado:
        raise HTTPException(status_code=404, detail="Barbeiro não encontrado.")

    return horarios_disponiveis

@router.patch("/{agendamento_id}/cancelar", response_model=AgendamentoResponse)
def cancelar_agendamento_router(agendamento_id: int, db: Session = Depends(get_db)):
    try:
        agendamento_cancelado = cancelar_agendamento(db, agendamento_id)
    except RecursoNaoEncontrado:
        raise HTTPException(status_code=404, detail="Recurso não encontrado")
    except OperacaoInvalida:
        raise HTTPException(status_code=400, detail="Operação inválida")

    return agendamento_cancelado
