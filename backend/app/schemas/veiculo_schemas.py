from pydantic import BaseModel, Field


class VeiculoBase(BaseModel):

    marca: str = Field(max_length=50)

    modelo: str = Field(max_length=50)

    ano: int

    placa: str = Field(max_length=10)

    cliente_id: int


class VeiculoCreate(VeiculoBase):
    pass


class VeiculoResponse(VeiculoBase):

    id: int

    cliente_nome: str

    class Config:
        from_attributes = True