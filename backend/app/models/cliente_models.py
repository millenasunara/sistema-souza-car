from sqlalchemy import Column, Integer, String

from app.database import Base

from sqlalchemy.orm import relationship

class Cliente(Base):

    __tablename__ = "clientes"


    id = Column(Integer, primary_key=True)

    nome = Column(String(100), nullable=False)

    telefone = Column(String(20))

    email = Column(String(100))

    veiculos = relationship("Veiculo", back_populates="cliente")