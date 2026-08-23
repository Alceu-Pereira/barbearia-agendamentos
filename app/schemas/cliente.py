from pydantic import BaseModel, ConfigDict

class ClienteBase(BaseModel):
    nome: str
    telefone: str

class ClienteCreate(ClienteBase):
    pass

class ClienteRead(ClienteBase):
    id: int
    ativo: bool

    model_config = ConfigDict(from_attributes=True)