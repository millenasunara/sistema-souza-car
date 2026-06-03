from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.veiculo_models import Veiculo
from app.models.cliente_models import Cliente

from app.schemas.veiculo_schemas import (
    VeiculoCreate,
    VeiculoResponse
)

router = APIRouter(
    prefix="/veiculos",
    tags=["Veículos"]
)


@router.post(
    "/",
    response_model=VeiculoResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_veiculo(
    veiculo: VeiculoCreate,
    db: Session = Depends(get_db)
):

    cliente_existe = (
        db.query(Cliente)
        .filter(Cliente.id == veiculo.cliente_id)
        .first()
    )

    if not cliente_existe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente com ID {veiculo.cliente_id} não encontrado."
        )

    placa_formatada = veiculo.placa.strip().upper()

    placa_existente = (
        db.query(Veiculo)
        .filter(Veiculo.placa == placa_formatada)
        .first()
    )

    if placa_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um veículo cadastrado com esta placa."
        )

    novo_veiculo = Veiculo(
        marca=veiculo.marca,
        modelo=veiculo.modelo,
        ano=veiculo.ano,
        placa=placa_formatada,
        cliente_id=veiculo.cliente_id
    )

    db.add(novo_veiculo)
    db.commit()
    db.refresh(novo_veiculo)

    return {
        "id": novo_veiculo.id,
        "marca": novo_veiculo.marca,
        "modelo": novo_veiculo.modelo,
        "ano": novo_veiculo.ano,
        "placa": novo_veiculo.placa,
        "cliente_id": novo_veiculo.cliente_id,
        "cliente_nome": cliente_existe.nome
    }


@router.get(
    "/",
    response_model=list[VeiculoResponse]
)
def listar_veiculos(
    db: Session = Depends(get_db)
):

    veiculos = db.query(Veiculo).all()

    resultado = []

    for veiculo in veiculos:

        resultado.append({

            "id": veiculo.id,

            "marca": veiculo.marca,

            "modelo": veiculo.modelo,

            "ano": veiculo.ano,

            "placa": veiculo.placa,

            "cliente_id": veiculo.cliente_id,

            "cliente_nome": veiculo.cliente.nome
        })

    return resultado


@router.get(
    "/cliente/{cliente_id}",
    response_model=list[VeiculoResponse]
)
def listar_veiculos_por_cliente(
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

    veiculos = (
        db.query(Veiculo)
        .filter(Veiculo.cliente_id == cliente_id)
        .all()
    )

    resultado = []

    for veiculo in veiculos:

        resultado.append({

            "id": veiculo.id,

            "marca": veiculo.marca,

            "modelo": veiculo.modelo,

            "ano": veiculo.ano,

            "placa": veiculo.placa,

            "cliente_id": veiculo.cliente_id,

            "cliente_nome": cliente.nome
        })

    return resultado


@router.get(
    "/{veiculo_id}",
    response_model=VeiculoResponse
)
def buscar_veiculo_por_id(
    veiculo_id: int,
    db: Session = Depends(get_db)
):

    veiculo = (
        db.query(Veiculo)
        .filter(Veiculo.id == veiculo_id)
        .first()
    )

    if not veiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veículo não encontrado."
        )

    return {

        "id": veiculo.id,

        "marca": veiculo.marca,

        "modelo": veiculo.modelo,

        "ano": veiculo.ano,

        "placa": veiculo.placa,

        "cliente_id": veiculo.cliente_id,

        "cliente_nome": veiculo.cliente.nome
    }


@router.put(
    "/{veiculo_id}",
    response_model=VeiculoResponse
)
def atualizar_veiculo(
    veiculo_id: int,
    veiculo_dados: VeiculoCreate,
    db: Session = Depends(get_db)
):

    veiculo_db = (
        db.query(Veiculo)
        .filter(Veiculo.id == veiculo_id)
        .first()
    )

    if not veiculo_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veículo não encontrado."
        )

    cliente = (
        db.query(Cliente)
        .filter(Cliente.id == veiculo_dados.cliente_id)
        .first()
    )

    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado."
        )

    placa_formatada = veiculo_dados.placa.strip().upper()

    placa_existe = (
        db.query(Veiculo)
        .filter(
            Veiculo.placa == placa_formatada,
            Veiculo.id != veiculo_id
        )
        .first()
    )

    if placa_existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um veículo cadastrado com esta placa."
        )

    veiculo_db.marca = veiculo_dados.marca
    veiculo_db.modelo = veiculo_dados.modelo
    veiculo_db.ano = veiculo_dados.ano
    veiculo_db.placa = placa_formatada
    veiculo_db.cliente_id = veiculo_dados.cliente_id

    db.commit()
    db.refresh(veiculo_db)

    return {
        "id": veiculo_db.id,
        "marca": veiculo_db.marca,
        "modelo": veiculo_db.modelo,
        "ano": veiculo_db.ano,
        "placa": veiculo_db.placa,
        "cliente_id": veiculo_db.cliente_id,
        "cliente_nome": cliente.nome
    }


@router.delete(
    "/{veiculo_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def deletar_veiculo(
    veiculo_id: int,
    db: Session = Depends(get_db)
):

    veiculo = (
        db.query(Veiculo)
        .filter(Veiculo.id == veiculo_id)
        .first()
    )

    if not veiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veículo não encontrado."
        )

    db.delete(veiculo)
    db.commit()

    return None