from datetime import datetime, timedelta, date, time

from app.database import SessionLocal

from app.models.enums import Estados
from app.models.agendamento import Agendamento
from app.schemas.agendamento import AgendamentoCreate

from app.services.barbeiro_service import buscar_barbeiro_por_id
from app.services.cliente_service import buscar_cliente_por_id
from app.services.servico_service import buscar_servico_por_id

from app.services.exceptions import RecursoNaoEncontrado, ConflitoDeHorario

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

    data_hora_fim = calcular_horario_fim(dados.data_hora_inicio, servico.duracao_minutos)

    conflito = verificar_conflito_horario(db, dados.barbeiro_id, dados.data_hora_inicio, data_hora_fim)

    if conflito:
        raise ConflitoDeHorario("Conflito de horário nos agendamentos")

    agendamento = Agendamento(
        cliente_id = dados.cliente_id,
        barbeiro_id = dados.barbeiro_id,
        servico_id = dados.servico_id,
        status = Estados.PENDENTE,
        data_hora_inicio = dados.data_hora_inicio,
        data_hora_fim = data_hora_fim,
        preco_cobrado = servico.preco
    )

    db.add(agendamento)
    db.commit()
    db.refresh(agendamento)
    
    return agendamento


def listar_disponibilidade(
        db: Session,
        barbeiro_id: int,
        data: date,
        ) -> list[datetime]:

    horario_abertura_barbearia = time(8, 0)
    horario_fechamento_barbearia = time(18, 0)
    slots_possiveis = []

    data_incrementada = datetime.combine(data, horario_abertura_barbearia)

    barbeiro = buscar_barbeiro_por_id(db, barbeiro_id)
    if barbeiro is None:
        raise RecursoNaoEncontrado("Barbeiro não encontrado")
    
    if data.weekday() == 0 or data.weekday() == 6:
        return []

    while data_incrementada < datetime.combine(data, horario_fechamento_barbearia):
        slots_possiveis.append(data_incrementada)
        data_incrementada += timedelta(minutes=30)

    return slots_possiveis