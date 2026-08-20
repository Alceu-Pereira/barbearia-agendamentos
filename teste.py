from sqlalchemy import create_engine, insert
from app.models.barbeiro import Barbeiro

engine_teste = create_engine("sqlite:///:memory:")
Barbeiro.metadata.create_all(engine_teste)

with engine_teste.connect() as conn:
    conn.execute(insert(Barbeiro).values(nome="Teste", telefone="123"))
    conn.commit()
    resultado = conn.execute(Barbeiro.__table__.select()).fetchone()
    print(resultado)

    print(resultado.ativo)
    print(type(resultado.ativo))