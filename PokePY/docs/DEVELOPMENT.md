# Guia de desenvolvimento

## Ambiente local

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Instalação:

```bash
pip install --upgrade pip
pip install -r requirements-dev.txt
```

## Comandos principais

```bash
python -m PokePY.main
uvicorn PokePY.api.main:app --reload
docker compose up --build
pytest
pytest --cov=PokePY --cov-report=term-missing
ruff check PokePY tests
black PokePY tests
mypy PokePY
```

## Makefile

```bash
make install-dev
make run-game
make run-api
make docker-up
make test
make coverage
make lint
make format
make migrate
```

## Banco de dados

Subir MySQL e API:

```bash
docker compose up --build
```

Executar migrations:

```bash
alembic upgrade head
```

Criar migration:

```bash
alembic revision --autogenerate -m "descricao_da_migration"
```

## Testes

```bash
pytest
```

Com cobertura:

```bash
pytest --cov=PokePY --cov-report=term-missing
```

## Qualidade

```bash
ruff check PokePY tests
black PokePY tests
mypy PokePY
```

## Pre-commit

```bash
pre-commit install
pre-commit run --all-files
```

## Fluxo recomendado

1. Criar branch.
2. Alterar código.
3. Rodar testes.
4. Rodar lint e formatação.
5. Atualizar documentação, se necessário.
6. Abrir pull request.
7. Aguardar CI passar.
