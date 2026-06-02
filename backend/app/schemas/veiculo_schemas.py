from pydantic import BaseModel, Field

# Schema Base com os atributos comuns para Veículo
class VeiculoBase(BaseModel):
    marca: str = Field(max_length=50)
    modelo: str = Field(max_length=50)
    ano: int
    placa: str = Field(max_length=10)
    cliente_id: int

# Criação de veículo
class VeiculoCreate(VeiculoBase):
    pass

# resposta da API (dados retornados ao cliente)
class VeiculoResponse(VeiculoBase):
    id: int

    class Config:
        # Permite que o Pydantic leia diretamente os objetos do SQLAlchemy
        from_attributes = True

