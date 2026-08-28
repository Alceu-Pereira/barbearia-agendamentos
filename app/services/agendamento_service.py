from datetime import datetime, timedelta

def calcular_horario_fim(data_hora_inicio: datetime, duracao_minutos: int) -> datetime:
    horario_fim = data_hora_inicio + timedelta(minutes=duracao_minutos)
    return horario_fim

