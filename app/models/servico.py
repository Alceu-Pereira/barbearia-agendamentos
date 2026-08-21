from app.database import Base

from decimal import Decimal

from sqlalchemy import String, Boolean, Numeric, Integer, true

from sqlalchemy.orm import Mapped, mapped_column

class Servico(Base):
    __tablename__ = "servicos"

    id: Mapped[int] = mapped_column(primary_key=True)
    ativo: Mapped[bool] = mapped_column(Boolean, server_default=true())
    nome: Mapped[str] = mapped_column(String(50))
    duracao_minutos: Mapped[int] = mapped_column(Integer)
    preco: Mapped[Decimal] = mapped_column(Numeric(10, 2))