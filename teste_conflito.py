from datetime import datetime
from app.database import SessionLocal
from app.schemas.agendamento import AgendamentoCreate
from app.services.agendamento_service import criar_agendamento
from app.services.exceptions import RecursoNaoEncontrado, ConflitoDeHorario

db = SessionLocal()

# Cenário 1: criação válida (ajuste os ids conforme o que já existe no seu banco)
dados = AgendamentoCreate(cliente_id=1, barbeiro_id=1, servico_id=1, data_hora_inicio=datetime(2026, 8, 24, 10, 0))
agendamento = criar_agendamento(db, dados)
print(agendamento.id, agendamento.status, agendamento.data_hora_fim, agendamento.preco_cobrado)

# Cenário 2: cliente inexistente
try:
    dados_invalidos = AgendamentoCreate(cliente_id=9999, barbeiro_id=1, servico_id=1, data_hora_inicio=datetime(2026, 8, 24, 11, 0))
    criar_agendamento(db, dados_invalidos)
except RecursoNaoEncontrado as e:
    print("Capturei:", e)

# Cenário 3: conflito de horário (mesmo horário do agendamento criado no Cenário 1)
try:
    dados_conflitantes = AgendamentoCreate(cliente_id=1, barbeiro_id=1, servico_id=1, data_hora_inicio=datetime(2026, 8, 24, 10, 0))
    criar_agendamento(db, dados_conflitantes)
except ConflitoDeHorario as e:
    print("Capturei:", e)