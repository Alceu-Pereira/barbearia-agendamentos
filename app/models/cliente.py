from app.database import Base

from sqlalchemy import String, Boolean

from sqlalchemy.orm import Mapped, mapped_column

class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(30))
    telefone: Mapped[str] = mapped_column(String(15))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)