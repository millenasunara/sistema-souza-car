from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OrdemServicoCreate(BaseModel):

    descricao_problema: str

    status: Optional[str] = None

    valor_total: float = 0.0

    veiculo_id: int

    data_abertura: Optional[datetime] = None


class OrdemServicoResponse(BaseModel):

    id: int

    descricao_problema: str

    status: str

    valor_total: float

    veiculo_id: int

    veiculo_modelo: str

    cliente_nome: str

    data_abertura: datetime

    class Config:
        from_attributes = True