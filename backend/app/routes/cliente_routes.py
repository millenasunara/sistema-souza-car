from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.cliente_models import Cliente

from app.schemas.cliente_schemas import (
    ClienteCreate,
    ClienteResponse
)


router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)


@router.post(
    "/",

    
    response_model=ClienteResponse
)
def criar_cliente(

    cliente: ClienteCreate,

    db: Session = Depends(get_db)
):

    novo_cliente = Cliente(
        nome=cliente.nome,
        telefone=cliente.telefone,
        email=cliente.email
    )
    db.add(novo_cliente)

    db.commit()

    db.refresh(novo_cliente)

    return novo_cliente


@router.get(
    "/",

    response_model=list[ClienteResponse]
)
def listar_clientes(

    db: Session = Depends(get_db)
):


    clientes = db.query(Cliente).all()

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
