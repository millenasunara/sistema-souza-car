from pydantic import BaseModel


class OrdemServicoCreate(BaseModel):
    descricao_problema: str
    status: str = "Pendente"
    valor_total: float = 0.0
    veiculo_id: int


class OrdemServicoResponse(BaseModel):
    id: int
    descricao_problema: str
    status: str
    valor_total: float
    veiculo_id: int

    class Config:
        from_attributes = True
