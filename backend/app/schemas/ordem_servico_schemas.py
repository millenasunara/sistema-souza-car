from pydantic import BaseModel
from typing import Optional


class OrdemServicoCreate(BaseModel):

    descricao_problema: str

    status: Optional[str] = None

    valor_total: float = 0.0

    veiculo_id: int


class OrdemServicoResponse(BaseModel):

    id: int

    descricao_problema: str

    status: str

    valor_total: float

    veiculo_id: int

    veiculo_modelo: str

    cliente_nome: str

    class Config:
        from_attributes = True