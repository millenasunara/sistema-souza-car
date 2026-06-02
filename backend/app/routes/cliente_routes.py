

# APIRouter -> cria grupo de rotas
# Depends -> injeta dependências
from fastapi import APIRouter, Depends

# Session -> conexão do SQLAlchemy
from sqlalchemy.orm import Session

# get_db -> função que abre conexão banco
from app.database import get_db

# Model SQLAlchemy
from app.models.cliente_models import Cliente

# Schemas Pydantic
from app.schemas.cliente_schemas import (
    ClienteCreate,
    ClienteResponse
)


router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)


# ROTA: CRIAR CLIENTE
@router.post(
    "/",

    # Define resposta da rota
    response_model=ClienteResponse
)
def criar_cliente(

    # Dados recebidos no body da requisição
    cliente: ClienteCreate,

    # Conexão banco
    db: Session = Depends(get_db)
):

    # Cria objeto Cliente usando dados recebidos

    novo_cliente = Cliente(
        nome=cliente.nome,
        telefone=cliente.telefone,
        email=cliente.email
    )

    # =====================================================
    # db.add()
    #
    # Adiciona objeto na sessão do banco
    # =====================================================

    db.add(novo_cliente)

    # =====================================================
    # db.commit()
    #
    # Salva definitivamente no banco
    # =====================================================

    db.commit()

    # =====================================================
    # db.refresh()
    #
    # Atualiza objeto com dados do banco
    #
    # Exemplo:
    # pega ID gerado automaticamente
    # =====================================================

    db.refresh(novo_cliente)

    # Retorna cliente criado
    return novo_cliente


# ROTA: LISTAR CLIENTES
@router.get(
    "/",

    # Lista de clientes
    response_model=list[ClienteResponse]
)
def listar_clientes(

    # Conexão banco
    db: Session = Depends(get_db)
):

    # Busca todos clientes
    # SELECT * FROM clientes

    clientes = db.query(Cliente).all()

    # Retorna lista
    return clientes

