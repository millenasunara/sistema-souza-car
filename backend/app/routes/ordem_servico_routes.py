from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.ordem_servico_models import OrdemServico
from app.models.veiculo_models import Veiculo
from app.schemas.ordem_servico_schemas import OrdemServicoCreate, OrdemServicoResponse


router = APIRouter(
    prefix="/ordens-servico",
    tags=["Ordens de Serviço"]
)


@router.post(
    "/",
    response_model=OrdemServicoResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_ordem_servico(
    ordem: OrdemServicoCreate,
    db: Session = Depends(get_db)
):
    veiculo_existe = db.query(Veiculo).filter(Veiculo.id == ordem.veiculo_id).first()
    if not veiculo_existe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Veículo com ID {ordem.veiculo_id} não existe."
        )

    nova_ordem = OrdemServico(
        descricao_problema=ordem.descricao_problema,
        status=ordem.status,
        valor_total=ordem.valor_total,
        veiculo_id=ordem.veiculo_id
    )

    db.add(nova_ordem)
    db.commit()
    db.refresh(nova_ordem)

    return nova_ordem


@router.get(
    "/",
    response_model=list[OrdemServicoResponse]
)
def listar_ordens_servico(
    db: Session = Depends(get_db)
):
    ordens = db.query(OrdemServico).all()
    return ordens


@router.get(
    "/{ordem_id}",
    response_model=OrdemServicoResponse
)
def buscar_ordem_por_id(
    ordem_id: int,
    db: Session = Depends(get_db)
):
    ordem = db.query(OrdemServico).filter(OrdemServico.id == ordem_id).first()
    if not ordem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ordem de serviço não encontrada."
        )
    return ordem


@router.put(
    "/{ordem_id}",
    response_model=OrdemServicoResponse
)
def atualizar_ordem_servico(
    ordem_id: int,
    ordem_dados: OrdemServicoCreate,
    db: Session = Depends(get_db)
):
    ordem_db = db.query(OrdemServico).filter(OrdemServico.id == ordem_id).first()
    if not ordem_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ordem de serviço não encontrada."
        )

    veiculo = db.query(Veiculo).filter(Veiculo.id == ordem_dados.veiculo_id).first()
    if not veiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Veículo com ID {ordem_dados.veiculo_id} não encontrado."
        )

    ordem_db.descricao_problema = ordem_dados.descricao_problema
    ordem_db.status = ordem_dados.status
    ordem_db.valor_total = ordem_dados.valor_total
    ordem_db.veiculo_id = ordem_dados.veiculo_id

    db.commit()
    db.refresh(ordem_db)
    return ordem_db


@router.delete(
    "/{ordem_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def deletar_ordem_servico(
    ordem_id: int,
    db: Session = Depends(get_db)
):
    ordem_db = db.query(OrdemServico).filter(OrdemServico.id == ordem_id).first()
    if not ordem_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ordem de serviço não encontrada."
        )

    db.delete(ordem_db)
    db.commit()

    return None
