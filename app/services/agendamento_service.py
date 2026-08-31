from datetime import datetime, timedelta

from app.database import SessionLocal

from app.models.enums import Estados
from app.models.agendamento import Agendamento
from app.schemas.agendamento import AgendamentoCreate

from app.services.barbeiro_service import buscar_barbeiro_por_id
from app.services.cliente_service import buscar_cliente_por_id
from app.services.servico_service import buscar_servico_por_id

from exceptions import RecursoNaoEncontrado, ConflitoDeHorario

from sqlalchemy.orm import Session
from sqlalchemy import select

def calcular_horario_fim(data_hora_inicio: datetime, duracao_minutos: int) -> datetime:
    horario_fim = data_hora_inicio + timedelta(minutes=duracao_minutos)
    return horario_fim

def verificar_conflito_horario(
            db: Session,
            barbeiro_id: int,
            data_hora_inicio: datetime,
            data_hora_fim: datetime) -> bool:
    stmt = select(Agendamento).where(Agendamento.barbeiro_id == barbeiro_id, Agendamento.status != Estados.CANCELADO)
    resultado = db.scalars(stmt).all()
    for agendamento in resultado:
       if not (data_hora_inicio >= agendamento.data_hora_fim or data_hora_fim <= agendamento.data_hora_inicio):
           return True
    return False

def criar_agendamento(
        db: Session,
        dados: AgendamentoCreate
) -> Agendamento:

    cliente = buscar_cliente_por_id(db, dados.cliente_id)
    if cliente is None:
        raise RecursoNaoEncontrado("Cliente não encontrado")

    barbeiro = buscar_barbeiro_por_id(db, dados.barbeiro_id)
    if barbeiro is None:
        raise RecursoNaoEncontrado("Barbeiro não encontrado")

    servico = buscar_servico_por_id(db, dados.servico_id)
    if servico is None:
        raise RecursoNaoEncontrado("Serviço não encontrado")