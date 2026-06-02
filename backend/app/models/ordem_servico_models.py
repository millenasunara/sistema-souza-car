# Importa os tipos de coluna do SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

# Importa a Base criada no database.py
from app.database import Base


# Classe que representa a tabela "ordens_servico"
class OrdemServico(Base):

    # Nome da tabela no banco Azure SQL
    __tablename__ = "ordens_servico"

    # COLUNAS DA TABELA

    # ID da ordem de serviço
    id = Column(Integer, primary_key=True, index=True)

    # Descrição do que precisa ser feito
    descricao_problema = Column(String(500), nullable=False)

    # Status do serviço (ex: Pendente, Em Andamento, Concluído)
    status = Column(String(50), default="Pendente")

    # Valor total do serviço
    valor_total = Column(Float, default=0.0)

    # CHAVE ESTRANGEIRA (Foreign Key)
    # Liga esta ordem de serviço ao ID de um veículo na tabela "veiculos"
    veiculo_id = Column(Integer, ForeignKey("veiculos.id"))

    # RELACIONAMENTO
    # Permite acessar os dados do veículo associado a esta ordem
    veiculo = relationship("Veiculo", back_populates="ordens_servico")
