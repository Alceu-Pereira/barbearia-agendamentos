from pydantic import BaseModel, ConfigDict

class BarbeiroBase(BaseModel):
    nome: str
    telefone: str

class BarbeiroCreate(BarbeiroBase):
    pass

class BarbeiroResponse(BarbeiroBase):
    id: int
    ativo: bool

    model_config = ConfigDict(from_attributes=True)