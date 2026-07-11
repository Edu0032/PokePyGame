# Deploy da API no Render com Supabase

## Arquitetura

```text
Executável PokePY -> FastAPI no Render -> Session Pooler -> PostgreSQL no Supabase
```

## Banco

No Supabase, copiar a URL do **Session Pooler**, porta `5432`, e adicionar SSL:

```text
postgresql://postgres.PROJECT_REF:SENHA@HOST.pooler.supabase.com:5432/postgres?sslmode=require
```

A conexão direta gratuita pode depender de IPv6. O pooler fornece a alternativa compatível sem colocar credenciais no repositório.

## Serviço Render

Criar um Web Service ligado ao repositório.

```text
Runtime: Python
Branch: main
Root Directory: vazio
```

Build:

```bash
pip install --upgrade pip && pip install -r requirements-api.txt
```

Start:

```bash
alembic upgrade head && uvicorn PokePY.api.main:app --host 0.0.0.0 --port $PORT
```

## Variáveis

```text
PYTHON_VERSION=3.11.15
DATABASE_URL=URL_DO_SESSION_POOLER
POKEPY_DATABASE_URL=URL_DO_SESSION_POOLER
POKEPY_AUTO_CREATE_TABLES=false
POKEPY_CORS_ORIGINS=["*"]
POKEPY_ENV=production
POKEPY_LOG_LEVEL=INFO
```

A URL do banco existe somente no Render.

Com wildcard CORS, a aplicação usa `allow_credentials=false`. Isso evita uma combinação insegura e desnecessária para o cliente desktop.

## Deploy da versão 5

As regras de matchmaking e combate são executadas na API. Após enviar a versão 5 ao GitHub, aguardar o auto-deploy do Render ou usar:

```text
Manual Deploy -> Deploy latest commit
```

Mudanças de dependências ou versão do Python podem exigir:

```text
Manual Deploy -> Clear build cache & deploy
```

## Verificação

```text
https://pokepygame.onrender.com/health
https://pokepygame.onrender.com/health/ready
https://pokepygame.onrender.com/docs
```

Resultado esperado de prontidão:

```json
{
  "status": "ok",
  "database": "ready"
}
```

Teste pelo repositório:

```powershell
python scripts/check_online_api.py
```

## Tabelas

As migrações Alembic criam:

```text
leaderboard_scores
player_progress
multiplayer_tickets
multiplayer_matches
multiplayer_actions
```

Não é necessário configurar RLS para este fluxo. O cliente não usa a API pública do Supabase; somente o backend se conecta ao PostgreSQL com a connection string privada.

## Cliente oficial

```powershell
python scripts/configure_api_url.py --api-url "https://pokepygame.onrender.com"
```

Configuração esperada:

```json
{
  "backend_mode": "api",
  "leaderboard_backend": "api",
  "progress_backend": "api",
  "multiplayer_backend": "api",
  "api_base_url": "https://pokepygame.onrender.com",
  "api_timeout_seconds": 65.0,
  "api_json_fallback": false
}
```

O fallback permanece desativado na release para que falhas online não sejam ocultadas por arquivos locais.
