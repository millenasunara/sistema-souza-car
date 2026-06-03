from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.ordem_servico_models import OrdemServico
from app.models.veiculo_models import Veiculo

from app.schemas.ordem_servico_schemas import (
    OrdemServicoCreate,
    OrdemServicoResponse
)

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

    veiculo = (
        db.query(Veiculo)
        .filter(Veiculo.id == ordem.veiculo_id)
        .first()
    )

    if not veiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veículo não encontrado."
        )

    nova_ordem = OrdemServico(

        descricao_problema=ordem.descricao_problema,

        status=(
            ordem.status
            if ordem.status
            else "Pendente"
        ),

        valor_total=ordem.valor_total,

        veiculo_id=ordem.veiculo_id
    )

    db.add(nova_ordem)

    db.commit()

    db.refresh(nova_ordem)

    return {
        "id": nova_ordem.id,
        "descricao_problema": nova_ordem.descricao_problema,
        "status": nova_ordem.status,
        "valor_total": nova_ordem.valor_total,
        "veiculo_id": nova_ordem.veiculo_id,
        "veiculo_modelo": veiculo.modelo,
        "cliente_nome": veiculo.cliente.nome
    }


@router.get(
    "/",
    response_model=list[OrdemServicoResponse]
)
def listar_ordens_servico(
    db: Session = Depends(get_db)
):

    ordens = db.query(OrdemServico).all()

    resultado = []

    for ordem in ordens:

        resultado.append({

            "id": ordem.id,

            "descricao_problema": ordem.descricao_problema,

            "status": ordem.status,

            "valor_total": ordem.valor_total,

            "veiculo_id": ordem.veiculo_id,

            "veiculo_modelo": ordem.veiculo.modelo,

            "cliente_nome": ordem.veiculo.cliente.nome
        })

    return resultado