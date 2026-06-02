
# =========================================================
# DATABASE.PY
# =========================================================
#
# Esse arquivo é responsável por:
#
# - conectar no Azure SQL
# - criar engine SQLAlchemy
# - criar sessões do banco
# - criar Base dos models
#
# Todo backend depende desse arquivo.
#
# =========================================================


# =========================================================
# IMPORTS
# =========================================================

# create_engine -> cria conexão banco
from sqlalchemy import create_engine

# sessionmaker -> cria sessões banco
# declarative_base -> base dos models
from sqlalchemy.orm import (
    sessionmaker,
    declarative_base
)

# load_dotenv -> lê variáveis do .env
from dotenv import load_dotenv

# os -> acessar variáveis ambiente
import os


# =========================================================
# CARREGA .ENV
# =========================================================
#
# Lê arquivo .env automaticamente
#
# Exemplo:
#
# DATABASE_URL=xxxxx
#
# =========================================================

load_dotenv()


# =========================================================
# PEGA STRING CONEXÃO
# =========================================================
#
# Busca variável DATABASE_URL do .env
#
# =========================================================

DATABASE_URL = os.getenv("DATABASE_URL")


# =========================================================
# ENGINE SQLALCHEMY
# =========================================================
#
# create_engine()
#
# Cria conexão principal com banco Azure SQL
#
# pool_pre_ping=True
#
# Verifica se conexão ainda está ativa
# antes de usar
#
# Evita erros de conexão caída
#
# =========================================================

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


# =========================================================
# SESSIONLOCAL
# =========================================================
#
# Cria sessões do banco
#
# Cada requisição FastAPI usa uma sessão
#
# =========================================================

SessionLocal = sessionmaker(

    # Não salva automaticamente
    autocommit=False,

    # Não atualiza automaticamente
    autoflush=False,

    # Usa engine criada acima
    bind=engine
)


# =========================================================
# BASE DOS MODELS
# =========================================================
#
# Todos models devem herdar dessa Base
#
# Exemplo:
#
# class Cliente(Base):
#
# =========================================================

Base = declarative_base()


# =========================================================
# DEPENDENCY DO FASTAPI
# =========================================================
#
# Função usada nas rotas:
#
# db: Session = Depends(get_db)
#
# Responsável por:
#
# - abrir conexão
# - entregar conexão rota
# - fechar conexão no final
#
# =========================================================

def get_db():

    # Cria sessão banco
    db = SessionLocal()

    try:

        # Entrega conexão para rota
        yield db

    finally:

        # Fecha conexão após request
        db.close()

