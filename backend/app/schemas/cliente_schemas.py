from pydantic import BaseModel, EmailStr

class ClienteCreate(BaseModel):

    nome: str
    telefone: str
    email: EmailStr


class ClienteResponse(BaseModel):
    id: int

    nome: str

    telefone: str

    email: EmailStr

    class Config:
        from_attributes = True

