from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from datetime import datetime

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


def buscar_ordem_ou_404(ordem_id: int, db: Session) -> OrdemServico:
    ordem = (
        db.query(OrdemServico)
        .options(
            joinedload(OrdemServico.veiculo)
            .joinedload(Veiculo.cliente)
        )
        .filter(OrdemServico.id == ordem_id)
        .first()
    )
    if not ordem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ordem de serviço não encontrada."
        )
    return ordem


def montar_resposta(ordem: OrdemServico) -> dict:
    return {
        "id": ordem.id,
        "descricao_problema": ordem.descricao_problema,
        "status": ordem.status,
        "valor_total": ordem.valor_total,
        "veiculo_id": ordem.veiculo_id,
        "veiculo_modelo": ordem.veiculo.modelo,
        "cliente_nome": ordem.veiculo.cliente.nome,
        "data_abertura": ordem.data_abertura,
        "data_atualizacao": ordem.data_atualizacao
    }


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
        status=ordem.status if ordem.status else "Pendente",
        valor_total=ordem.valor_total,
        veiculo_id=ordem.veiculo_id,
        data_abertura=ordem.data_abertura if ordem.data_abertura else datetime.now()
    )

    db.add(nova_ordem)
    db.commit()
    db.refresh(nova_ordem)

    return montar_resposta(nova_ordem)


@router.get(
    "/",
    response_model=list[OrdemServicoResponse]
)
def listar_ordens_servico(
    db: Session = Depends(get_db)
):
    ordens = (
        db.query(OrdemServico)
        .options(
            joinedload(OrdemServico.veiculo)
            .joinedload(Veiculo.cliente)
        )
        .all()
    )

    return [montar_resposta(o) for o in ordens]


@router.get(
    "/{ordem_id}",
    response_model=OrdemServicoResponse
)
def buscar_ordem_servico(
    ordem_id: int,
    db: Session = Depends(get_db)
):
    return montar_resposta(buscar_ordem_ou_404(ordem_id, db))


@router.put(
    "/{ordem_id}",
    response_model=OrdemServicoResponse
)
def atualizar_ordem_servico(
    ordem_id: int,
    ordem: OrdemServicoCreate,
    db: Session = Depends(get_db)
):
    ordem_db = buscar_ordem_ou_404(ordem_id, db)

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

    ordem_db.descricao_problema = ordem.descricao_problema
    ordem_db.status = ordem.status
    ordem_db.valor_total = ordem.valor_total
    ordem_db.veiculo_id = ordem.veiculo_id
    ordem_db.data_atualizacao = datetime.now()

    db.commit()
    db.refresh(ordem_db)

    return montar_resposta(ordem_db)


@router.delete(
    "/{ordem_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def deletar_ordem_servico(
    ordem_id: int,
    db: Session = Depends(get_db)
):
    ordem = buscar_ordem_ou_404(ordem_id, db)
    db.delete(ordem)
    db.commit()


@router.get("/dashboard")
def dashboard_ordens(
    db: Session = Depends(get_db)
):
    ordens = db.query(OrdemServico).all()

    total_ordens = len(ordens)
    pendentes = len([o for o in ordens if o.status == "Pendente"])
    em_andamento = len([o for o in ordens if o.status == "Em Andamento"])
    concluidas = len([o for o in ordens if o.status == "Concluído"])
    faturamento_total = sum(
        o.valor_total for o in ordens if o.status == "Concluído"
    )

    return {
        "total_ordens": total_ordens,
        "pendentes": pendentes,
        "em_andamento": em_andamento,
        "concluidas": concluidas,
        "faturamento_total": faturamento_total
    }