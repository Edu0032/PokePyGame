# Guia de execução pelo código-fonte

## Pré-requisitos

- Python 3.11 ou superior.
- Git.
- Docker Desktop para API + banco local.
- Editor de código, como VS Code ou PyCharm.

## Clonar o repositório

```bash
git clone https://github.com/seu-usuario/pokepy.git
cd pokepy
```

## Criar ambiente virtual

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

## Instalar dependências

```bash
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

## Rodar somente o jogo com JSON local

```bash
python -m PokePY.main
```

## Rodar API e MySQL localmente

```bash
docker compose up --build
```

API local:

```text
http://127.0.0.1:8000
```

Docs da API:

```text
http://127.0.0.1:8000/docs
```

## Rodar o jogo conectado à API local

Windows PowerShell:

```powershell
.\scripts\run_game_online.ps1 -ApiUrl "http://127.0.0.1:8000"
```

Linux/macOS:

```bash
./scripts/run_game_online.sh http://127.0.0.1:8000
```

## Rodar testes

```bash
pytest
```

Com cobertura:

```bash
pytest --cov=PokePY --cov-report=term-missing
```

## Ferramentas de qualidade

```bash
ruff check PokePY tests
black --check PokePY tests
mypy PokePY
```
