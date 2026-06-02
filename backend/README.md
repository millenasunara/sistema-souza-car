# Sistema Souza Car - Backend

Backend do sistema de gerenciamento de oficina mecânica desenvolvido utilizando:

- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Azure SQL (futuramente)
- Swagger

---

#  Pré-requisitos

Antes de rodar o projeto, é necessário instalar os seguintes softwares na máquina.

---

# Python

Versão recomendada:

```bash
Python 3.14.4
```


## IMPORTANTE

Durante a instalação do Python:

- Marque a opção:

```txt
Add Python to PATH
```

---

## Verificar instalação

Após instalar:

```bash
python --version
```

ou

```bash
py --version
```

---


---

# VS Code

Editor utilizado para desenvolvimento.

---

## Extensões recomendadas

- Python
- Pylance

---

# ODBC Driver 18 for SQL Server

Necessário futuramente para conexão com Azure SQL.

Mesmo usando SQLite inicialmente, recomenda-se instalar desde já.

---

## Download ODBC Driver 18

https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server

---

## Verificar instalação do ODBC

Após instalar:

### Windows

Abrir:

```txt
ODBC Data Sources (64-bit)
```

Verificar se existe:

```txt
ODBC Driver 18 for SQL Server
```

---

# Estrutura do Projeto

```txt
backend/
│
├── app/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── cliente.py
│   │   ├── veiculo.py
│   │   └── ordem_servico.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── cliente_routes.py
│   │   ├── veiculo_routes.py
│   │   └── ordem_servico_routes.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── cliente.py
│   │   ├── veiculo.py
│   │   └── ordem_servico.py
│   │
│   ├── database.py
│   └── main.py
│
├── venv/
├── .env
├── requirements.txt
└── README.md
```

---

# Como Rodar o Projeto

---

# 1 - Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
```

---

# 2 - Entrar na pasta backend

```bash
cd backend
```

---

# 3 - Criar ambiente virtual

## Windows

```bash
python -m venv venv
```

---

# 4 - Ativar ambiente virtual

## Windows PowerShell

```bash
venv\Scripts\activate
```

Se funcionar corretamente, aparecerá:

```bash
(venv)
```

no início do terminal.

---

# 5 - Instalar dependências

```bash
pip install -r requirements.txt
```

---

# 6 - Criar arquivo `.env`

Na raiz do backend:

```txt
backend/
│
├── .env
```

---

# Conteúdo inicial do `.env`

## SQLite (Inicial)

```env
DATABASE_URL=sqlite:///./souza_car.db
```

---

# Configuração futura Azure SQL

Quando o sistema migrar para Azure SQL:

```env
DATABASE_URL=mssql+pyodbc://usuario:senha@servidor.database.windows.net/souza_car?driver=ODBC+Driver+18+for+SQL+Server
```

---

# IMPORTANTE SOBRE AZURE SQL

Para funcionar corretamente será necessário:

- Instalar ODBC Driver 18  
- Liberar IP no Firewall da Azure  
- Criar database na Azure  
- Criar usuário e senha SQL Server  

---

# 7 - Rodar o projeto

```bash
uvicorn app.main:app --reload
```

---

# API funcionando

Se tudo estiver correto:

```bash
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

# Swagger

Acessar no navegador:

```txt
http://127.0.0.1:8000/docs
```

Swagger permite:
- visualizar endpoints
- testar requisições
- enviar JSON
- validar respostas
- testar backend sem frontend

---


# Dependências do Projeto

Arquivo:

```txt
requirements.txt
```

Conteúdo:

```txt
fastapi 
uvicorn
sqlalchemy
pydantic
python-dotenv
pyodbc
pymssql
alembic
```

---

# Comandos Úteis

---

## Instalar nova biblioteca

```bash
pip install NOME_LIB
```

---

## Atualizar requirements.txt

```bash
pip freeze > requirements.txt
```

---

## Desativar ambiente virtual

```bash
deactivate
```