from decimal import Decimal
from datetime import datetime


from app.database import SessionLocal
from app.models.agendamento import Agendamento
from app.models.enums import Estados
from app.services.agendamento_service import verificar_conflito_horario

db = SessionLocal()

existente = Agendamento(
    cliente_id=1, barbeiro_id=1, servico_id=1,
    status=Estados.PENDENTE,
    data_hora_inicio=datetime(2026, 8, 23, 14, 30),
    data_hora_fim=datetime(2026, 8, 23, 15, 0),
    preco_cobrado=Decimal("29.90"),
)
db.add(existente)
db.commit()


cenarios = {
    "Cenario 1 (meio, deveria ser True)": (datetime(2026, 8, 23, 14, 45), datetime(2026, 8, 23, 15, 15)),
    "Cenario 2 (back-to-back, deveria ser False)": (datetime(2026, 8, 23, 15, 0), datetime(2026, 8, 23, 15, 30)),
    "Cenario 3 (dentro, deveria ser True)": (datetime(2026, 8, 23, 14, 40), datetime(2026, 8, 23, 14, 50)),
    "Cenario 4 (sem sobreposicao, deveria ser False)": (datetime(2026, 8, 23, 16, 0), datetime(2026, 8, 23, 16, 30)),
    "Cenário 5 (exatamente o mesmo horário, deveria ser True)": (existente.data_hora_inicio, existente.data_hora_fim),
}

for nome, (inicio, fim) in cenarios.items():
    resultado = verificar_conflito_horario(db, 1, inicio, fim)
    print(f"{nome}: {resultado}")