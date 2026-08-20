from app.database import Base

from sqlalchemy import String, Boolean, true

from sqlalchemy.orm import Mapped, mapped_column

class Barbeiro(Base):
    __tablename__ = "barbeiros"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(50))
    telefone: Mapped[str] = mapped_column(String(15))
    ativo: Mapped[bool] = mapped_column(Boolean, server_default=true())