from pydantic import BaseModel, ConfigDict

from decimal import Decimal

class ServicoBase(BaseModel):
    nome: str
    duracao_minutos: int
    preco: Decimal

class ServicoCreate(ServicoBase):
    pass

class ServicoResponse(ServicoBase):
    id: int
    ativo: bool
    model_config = ConfigDict(from_attributes=True)