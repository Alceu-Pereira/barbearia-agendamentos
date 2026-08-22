from app.models.servico import Servico
from app.models.barbeiro import Barbeiro
from app.models.cliente import Cliente

from app.database import Base

from sqlalchemy import ForeignKey, Enum as SQLEnum

from sqlalchemy.orm import Mapped, mapped_column
from app.models.enums import Estados

class Agendamento(Base):
    __tablename__ = "agendamentos"

    id: Mapped[int] = mapped_column(primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"))
    barbeiro_id: Mapped[int] = mapped_column(ForeignKey("barbeiros.id"))
    servico_id: Mapped[int] = mapped_column(ForeignKey("servicos.id"))
    status: Mapped[Estados] = mapped_column(SQLEnum(Estados, create_constraint=True), default=Estados.PENDENTE)