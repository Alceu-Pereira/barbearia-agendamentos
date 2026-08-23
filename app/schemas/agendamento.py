from pydantic import BaseModel, ConfigDict

from datetime import datetime
from decimal import Decimal
from app.models.enums import Estados

class AgendamentoBase(BaseModel):
    cliente_id: int
    barbeiro_id: int
    servico_id: int
    data_hora_inicio: datetime

class AgendamentoCreate(AgendamentoBase):
    pass

class AgendamentoResponse(AgendamentoBase):
    id: int
    data_hora_fim: datetime
    preco_cobrado: Decimal
    status: Estados
    model_config = ConfigDict(from_attributes=True)