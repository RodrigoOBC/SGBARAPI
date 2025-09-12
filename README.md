# FastAPI Template

## Licença e atribuição

Este projeto é distribuído sob uma licença customizada. É proibida a revenda deste código sem atribuição explícita a RodrigoOBC (ou CabralQA). Veja o arquivo LICENSE para detalhes.

## Estrutura

- `app/main.py`: Ponto de entrada da aplicação FastAPI
- `app/api/`: Rotas e endpoints
- `app/core/`: Configurações e utilitários
- `app/db/`: Sessão e conexão com banco de dados
- `app/models/`: Modelos SQLAlchemy
- `app/schemas/`: Schemas Pydantic

## Como rodar

1. Crie e ative o ambiente virtual (já criado em `.venv`)
2. Instale as dependências:
   ```bash
   /home/rodrigo_cabral/SGBARAPI/.venv/bin/pip install -r requirements.txt
   ```
3. Configure o banco de dados no arquivo `.env`
4. Inicie o servidor:
   ```bash
   /home/rodrigo_cabral/SGBARAPI/.venv/bin/uvicorn app.main:app --reload
   ```

## Dependências principais
- fastapi
- uvicorn
- sqlalchemy
- asyncpg
- psycopg2-binary

## Exemplo de endpoint
Acesse `GET /ping` para testar se a API está funcionando.
