# IMPORTAÇÃO FASTAPI
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

# IMPORTAÇÃO BANCO DE DADOS
from app.database import engine, Base
from app.models import cliente_models, veiculo_models, ordem_servico_models

# IMPORTAÇÃO DAS ROTAS
from app.routes import (
    cliente_routes,
    veiculo_routes,
    ordem_servico_routes
)

# CRIAÇÃO DAS TABELAS (BANCO DE DADOS)
# Lê todos os modelos importados e cria as tabelas fisicamente na Azure
Base.metadata.create_all(bind=engine)



# CRIAÇÃO DA API
app = FastAPI(
    title="Souza Car API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROTA TESTE
@app.get("/")
def home():

    return {
        "message": "API Souza Car funcionando"
    }

# INCLUSÃO DAS ROTAS
app.include_router(cliente_routes.router)
app.include_router(veiculo_routes.router)
app.include_router(ordem_servico_routes.router)
