from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class OrdemServico(Base):

    __tablename__ = "ordens_servico"

    id = Column(Integer, primary_key=True, index=True)

    descricao_problema = Column(String(500), nullable=False)

    status = Column(String(50), default="Pendente", index=True)

    valor_total = Column(Float, default=0.0)

    data_abertura = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    data_atualizacao = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    veiculo_id = Column(
        Integer,
        ForeignKey("veiculos.id"),
        index=True
    )

    veiculo = relationship(
        "Veiculo",
        back_populates="ordens_servico",
        lazy="joined"
    )