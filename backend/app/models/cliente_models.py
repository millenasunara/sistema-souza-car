# Importa os tipos de coluna do SQLAlchemy
from sqlalchemy import Column, Integer, String

# Importa a Base criada no database.py
# Toda tabela do banco deve herdar dela
from app.database import Base

# Importa o relationship para navegação entre tabelas
from sqlalchemy.orm import relationship


# Classe que representa a tabela "clientes"
class Cliente(Base):

    # Nome da tabela no banco Azure SQL
    __tablename__ = "clientes"

    # COLUNAS DA TABELA

    # ID do cliente
    # primary_key=True -> chave primária
    id = Column(Integer, primary_key=True)

    # Nome do cliente
    # String(100) -> máximo de 100 caracteres
    # nullable=False -> obrigatório
    nome = Column(String(100), nullable=False)

    # Telefone do cliente
    telefone = Column(String(20))

    # Email do cliente
    email = Column(String(100))

    # Relacionamento: Um cliente pode possuir vários veículos
    veiculos = relationship("Veiculo", back_populates="cliente")