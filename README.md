# Barbearia APP

Sistema de agendamentos para barbearia, desenvolvido para estudo.

## Tecnologias
Python, FastAPI, SQLAlchemy e SQLite(futuramente migraremos para PostgreSQL)

## Como rodar

1. Clone o repositório e entre na pasta:
```bash
git clone https://github.com/Alceu-Pereira/barbearia-agendamentos
cd barbearia-agendamentos
```

2. Crie e ative o ambiente virutal:
```bash
py -m venv .venv
.venv\Scripts\activate
```

3. Crie o arquivo `.env` a partir do `.env.example` e preencha a variável do banco de dados.

4. Instale as dependências e inicie o servidor:
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

5. Acesse a documentação interativa da API em `http://127.0.0.1:8000/docs`

