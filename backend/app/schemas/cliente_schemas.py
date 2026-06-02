
# Base principal do Pydantic
from pydantic import BaseModel, EmailStr

class ClienteCreate(BaseModel):

    # Nome obrigatório
    nome: str

    # Telefone obrigatório
    telefone: str

    # Email validado automaticamente
    # Se não for email válido -> FastAPI retorna erro
    email: EmailStr


class ClienteResponse(BaseModel):

    # ID gerado pelo banco
    id: int

    nome: str

    telefone: str

    email: EmailStr

    # from_attributes=True
    # Permite converter automaticamente:

    # SQLAlchemy -> JSON

    # Sem isso o FastAPI pode dar erro
    # ao retornar objetos do banco

    class Config:
        from_attributes = True

