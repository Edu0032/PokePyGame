# Uso da API REST

A API REST funciona como backend independente do cliente Pygame. Ela centraliza ranking, progresso do jogador e multiplayer.

## Rodar com Docker Compose

```bash
docker compose up --build
```

Serviços disponíveis:

```text
API   -> http://127.0.0.1:8000
Docs  -> http://127.0.0.1:8000/docs
MySQL -> 127.0.0.1:3306
```

## Rodar manualmente

Instalar dependências:

```bash
pip install -r requirements-api.txt
```

Configurar banco:

```bash
export POKEPY_DATABASE_URL="mysql+pymysql://pokepy_user:pokepy_password@127.0.0.1:3306/pokepy"
```

Rodar API:

```bash
uvicorn PokePY.api.main:app --reload
```

## Variáveis de ambiente

| Variável | Descrição |
|---|---|
| `POKEPY_DATABASE_URL` | URL de conexão SQLAlchemy |
| `POKEPY_API_BASE_URL` | URL usada pelo cliente Pygame |
| `POKEPY_LEADERBOARD_BACKEND` | Define backend do ranking: `json` ou `api` |
| `POKEPY_PROGRESS_BACKEND` | Define backend do progresso: `json` ou `api` |
| `POKEPY_LOG_LEVEL` | Nível de log da API |

## Conectar jogo à API

Windows PowerShell:

```powershell
$env:POKEPY_LEADERBOARD_BACKEND="api"
$env:POKEPY_PROGRESS_BACKEND="api"
$env:POKEPY_API_BASE_URL="http://127.0.0.1:8000"
python -m PokePY.main
```

Linux/macOS:

```bash
export POKEPY_LEADERBOARD_BACKEND="api"
export POKEPY_PROGRESS_BACKEND="api"
export POKEPY_API_BASE_URL="http://127.0.0.1:8000"
python -m PokePY.main
```

## Testar pelo navegador

Abrir:

```text
http://127.0.0.1:8000/docs
```

A interface permite testar endpoints diretamente pelo navegador.

## Testar com curl

Health:

```bash
curl http://127.0.0.1:8000/health
```

Ranking:

```bash
curl -X POST http://127.0.0.1:8000/leaderboard \
  -H "Content-Type: application/json" \
  -d '{"player_name":"Ana","elapsed_seconds":120}'
```
