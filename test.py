from sqlalchemy import create_engine, insert
from app.models.servico import Servico
from decimal import Decimal

engine_teste = create_engine("sqlite:///:memory:")
Servico.metadata.create_all(engine_teste)

with engine_teste.connect() as conn:
    conn.execute(insert(Servico).values(nome="Teste", duracao_minutos=30, preco=29.90))
    conn.commit()
    resultado = conn.execute(Servico.__table__.select()).fetchone()
    print(resultado)
    print(type(resultado.preco))