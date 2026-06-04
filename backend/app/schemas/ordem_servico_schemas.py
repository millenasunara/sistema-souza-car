from pydantic import BaseModel, field_serializer
from typing import Optional
from datetime import datetime

from app.datetime import to_brazil_time


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

    data_atualizacao: datetime

    class Config:
        from_attributes = True

    @field_serializer("data_abertura", "data_atualizacao")
    def serialize_datetimes(self, value: datetime):
        return to_brazil_time(value)