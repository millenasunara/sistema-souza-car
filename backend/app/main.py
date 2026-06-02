# IMPORTAÇÃO FASTAPI
from fastapi import FastAPI

# IMPORTAÇÃO DAS ROTAS
from app.routes import (
    cliente_routes,
    veiculo_routes,
    ordem_servico_routes
)

# CRIAÇÃO DA API
app = FastAPI(
    title="Souza Car API"
)

# ROTA TESTE
@app.get("/")
def home():

    return {
        "message": "API Souza Car funcionando"
    }

# INCLUSÃO DAS ROTAS
# app.include_router(cliente_routes.router)
# app.include_router(veiculo_routes.router)
# app.include_router(ordem_servico_routes.router)