from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Veiculo(Base):
    __tablename__ = "veiculos"

    # =========================
    # CAMPOS PRINCIPAIS
    # =========================

    id = Column(Integer, primary_key=True, index=True)

    marca = Column(String(50), nullable=False)
    modelo = Column(String(50), nullable=False)
    ano = Column(Integer, nullable=False)

    # placa normalizada (UPPER no backend)
    placa = Column(String(10), nullable=False, unique=True)

    # =========================
    # RELACIONAMENTO (FK)
    # =========================

    cliente_id = Column(
        Integer,
        ForeignKey("clientes.id"),
        nullable=False
    )

    # =========================
    # RELACIONAMENTO ORM
    # =========================

    cliente = relationship(
        "Cliente",
        back_populates="veiculos"
    )