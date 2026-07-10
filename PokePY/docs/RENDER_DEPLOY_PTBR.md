# Deploy da API no Render com banco Supabase

## Arquitetura de produção

```text
Executável PokePY -> API FastAPI no Render -> PostgreSQL no Supabase
```

O executável não contém banco de dados. O cliente envia requisições HTTP para a API hospedada. A API aplica regras de ranking, progresso e multiplayer e persiste os dados no PostgreSQL.

## Pré-requisitos

- Repositório `PokePyGame` no GitHub.
- Conta no Render.
- Projeto criado no Supabase.
- URL do **Session Pooler** do Supabase.

## 1. Configurar banco no Supabase

No Supabase, abrir o projeto e acessar:

```text
Connect -> Session Pooler
```

Usar a URL no formato:

```text
postgresql://postgres.PROJECT_REF:SENHA@aws-1-us-east-2.pooler.supabase.com:5432/postgres?sslmode=require
```

Pontos importantes:

- A conexão direta `db.PROJECT_REF.supabase.co` usa IPv6 por padrão em projetos gratuitos.
- A API no Render deve usar o pooler, que funciona para conexões IPv4.
- A porta recomendada para backend persistente é `5432` no **Session Pooler**.
- A senha do banco nunca deve ser enviada ao GitHub.

## 2. Configurar serviço web no Render

Criar um **Web Service** apontando para o repositório `PokePyGame`.

Configurações principais:

```text
Runtime: Python
Branch: main
Root Directory: vazio, se o projeto estiver na raiz
```

Build Command:

```bash
pip install --upgrade pip && pip install -r requirements-api.txt
```

Start Command:

```bash
alembic upgrade head && uvicorn PokePY.api.main:app --host 0.0.0.0 --port $PORT
```

O arquivo `render.yaml` já mantém essa configuração no repositório.

## 3. Variáveis de ambiente no Render

Adicionar em **Environment**:

```text
PYTHON_VERSION=3.11.15
POKEPY_DATABASE_URL=postgresql://postgres.PROJECT_REF:SENHA@aws-1-us-east-2.pooler.supabase.com:5432/postgres?sslmode=require
DATABASE_URL=postgresql://postgres.PROJECT_REF:SENHA@aws-1-us-east-2.pooler.supabase.com:5432/postgres?sslmode=require
POKEPY_AUTO_CREATE_TABLES=false
POKEPY_CORS_ORIGINS=["*"]
POKEPY_ENV=production
POKEPY_LOG_LEVEL=INFO
```

`DATABASE_URL` e `POKEPY_DATABASE_URL` podem receber o mesmo valor. A aplicação prioriza `POKEPY_DATABASE_URL`, mas aceita `DATABASE_URL` como fallback.

## 4. Fazer deploy limpo

Depois de alterar variáveis ou versão do Python:

```text
Manual Deploy -> Clear build cache & deploy
```

Esse passo evita que o Render reutilize dependências ou versão de Python antigas.

## 5. Validar a API

Com a URL pública da API:

```text
https://pokepygame.onrender.com
```

Testar no navegador:

```text
https://pokepygame.onrender.com/health
https://pokepygame.onrender.com/health/ready
https://pokepygame.onrender.com/docs
```

Resultado esperado para `/health`:

```json
{"status":"ok"}
```

`/health/ready` valida API e banco. `/docs` abre a documentação interativa da API.

## 6. Configurar o cliente para usar a API hospedada

No computador local, na raiz do projeto:

```bash
python scripts/configure_api_url.py --api-url "https://pokepygame.onrender.com"
```

Esse comando atualiza:

```text
pokepy_client.json
packaging/pokepy_client.json
```

Esses arquivos podem ir para o GitHub porque contêm apenas a URL pública da API.

## 7. Testar o cliente contra a API hospedada

Windows:

```powershell
.\scripts\run_game_online.ps1 -ApiUrl "https://pokepygame.onrender.com"
```

Linux/macOS:

```bash
./scripts/run_game_online.sh "https://pokepygame.onrender.com"
```

Testes práticos recomendados:

1. Abrir o jogo.
2. Criar treinador.
3. Vencer ou perder uma partida.
4. Verificar ranking.
5. Abrir duas instâncias do jogo.
6. Entrar no modo online nas duas.
7. Confirmar matchmaking e envio de ações.

## 8. Observação sobre plano gratuito

Serviços gratuitos podem ficar inativos após algum tempo sem uso. A primeira requisição após inatividade pode demorar alguns segundos. O cliente usa timeout e fallback local para preservar a experiência durante testes.
