

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.veiculo_models import Veiculo
from app.models.cliente_models import Cliente
from app.schemas.veiculo_schemas import VeiculoCreate, VeiculoResponse


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
    # 1. Validação: Verifica se o cliente (proprietário) existe no banco

    cliente_existe = db.query(Cliente).filter(Cliente.id == veiculo.cliente_id).first()
    if not cliente_existe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Não foi possível cadastrar o veículo: Cliente com ID {veiculo.cliente_id} não existe."
        )

    # 2. Validação: Verifica se a placa já está cadastrada (evita duplicidade)

    placa_formatada = veiculo.placa.strip().upper()
    veiculo_existente = db.query(Veiculo).filter(Veiculo.placa == placa_formatada).first()
    if veiculo_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um veículo cadastrado com esta placa."
        )

    # Cria objeto Veiculo usando dados recebidos
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

    return novo_veiculo


@router.get(
    "/",
    response_model=list[VeiculoResponse]
)
def listar_veiculos(
    db: Session = Depends(get_db)
):
    veiculos = db.query(Veiculo).all()
    return veiculos


@router.get(
    "/{veiculo_id}",
    response_model=VeiculoResponse
)
def buscar_veiculo_por_id(
    veiculo_id: int,
    db: Session = Depends(get_db)
):
    veiculo = db.query(Veiculo).filter(Veiculo.id == veiculo_id).first()
    if not veiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veículo não encontrado."
        )
    return veiculo


@router.put(
    "/{veiculo_id}",
    response_model=VeiculoResponse
)
def atualizar_veiculo(
    veiculo_id: int,
    veiculo_dados: VeiculoCreate,
    db: Session = Depends(get_db)
):
    veiculo_db = db.query(Veiculo).filter(Veiculo.id == veiculo_id).first()
    if not veiculo_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veículo não encontrado."
        )

    cliente = db.query(Cliente).filter(Cliente.id == veiculo_dados.cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Não foi possível cadastrar o veículo: Cliente com ID {veiculo_dados.cliente_id} não encontrado."
        )

    veiculo_db.marca = veiculo_dados.marca
    veiculo_db.modelo = veiculo_dados.modelo
    veiculo_db.ano = veiculo_dados.ano
    veiculo_db.placa = veiculo_dados.placa.strip().upper()
    veiculo_db.cliente_id = veiculo_dados.cliente_id

    db.commit()
    db.refresh(veiculo_db)
    return veiculo_db


@router.delete(
    "/{veiculo_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def deletar_veiculo(
    veiculo_id: int,
    db: Session = Depends(get_db)
):
    veiculo_db = db.query(Veiculo).filter(Veiculo.id == veiculo_id).first()
    if not veiculo_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veículo não encontrado."
        )

    db.delete(veiculo_db)
    db.commit()

    return None


