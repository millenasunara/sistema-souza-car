from fastapi import APIRouter, Depends, HTTPException, status



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

@router.get(
    "/{cliente_id}",
    response_model=ClienteResponse
)
def buscar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):

    cliente = (
        db.query(Cliente)
        .filter(Cliente.id == cliente_id)
        .first()
    )

    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado."
        )

    return cliente
@router.put(
    "/{cliente_id}",
    response_model=ClienteResponse
)
def atualizar_cliente(
    cliente_id: int,
    cliente: ClienteCreate,
    db: Session = Depends(get_db)
):

    cliente_db = (
        db.query(Cliente)
        .filter(Cliente.id == cliente_id)
        .first()
    )

    if not cliente_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado."
        )

    cliente_db.nome = cliente.nome
    cliente_db.telefone = cliente.telefone
    cliente_db.email = cliente.email

    db.commit()

    db.refresh(cliente_db)

    return cliente_db
@router.delete(
    "/{cliente_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def deletar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):

    cliente = (
        db.query(Cliente)
        .filter(Cliente.id == cliente_id)
        .first()
    )

    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado."
        )

    db.delete(cliente)

    db.commit()
