from fastapi import APIRouter, HTTPException, Depends

from app.schemas.agendamento import AgendamentoCreate, AgendamentoResponse

from app.services.agendamento_service import criar_agendamento

from app.services.exceptions import RecursoNaoEncontrado, ConflitoDeHorario, OperacaoInvalida

from sqlalchemy.orm import Session
from app.database import get_db

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

