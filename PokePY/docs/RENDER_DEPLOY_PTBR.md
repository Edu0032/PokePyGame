# Deploy da API no Render

## Pré-requisitos

- Conta no GitHub.
- Repositório PokePyGame enviado ao GitHub.
- Conta no Render.
- Arquivo `render.yaml` na raiz do repositório.

## Estrutura usada no deploy

```text
Cliente PokePY -> API FastAPI no Render -> PostgreSQL gerenciado no Render
```

O banco não fica no executável. O executável usa HTTP para conversar com a API hospedada.

## Passo 1 — Enviar o projeto ao GitHub

```bash
git init
git add .
git commit -m "Initial PokePY portfolio release"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/PokePyGame.git
git push -u origin main
```

## Passo 2 — Criar o Blueprint no Render

1. Entrar no painel do Render.
2. Selecionar **New +**.
3. Selecionar **Blueprint**.
4. Conectar o repositório `PokePyGame`.
5. Confirmar o arquivo `render.yaml`.
6. Aplicar o Blueprint.

O Render deve criar:

- serviço web `pokepy-api`;
- banco PostgreSQL `pokepy-db`;
- variável `POKEPY_DATABASE_URL` apontando para o banco;
- health check em `/health`.

## Passo 3 — Conferir variáveis de ambiente

Variáveis principais:

```env
POKEPY_DATABASE_URL=<gerado pelo Render>
POKEPY_AUTO_CREATE_TABLES=false
POKEPY_LOG_LEVEL=INFO
POKEPY_CORS_ORIGINS=["*"]
```

## Passo 4 — Conferir se a API subiu

Abrir no navegador:

```text
https://SEU-SERVICO.onrender.com/health
https://SEU-SERVICO.onrender.com/health/ready
https://SEU-SERVICO.onrender.com/docs
```

Resultado esperado para `/health`:

```json
{"status":"ok"}
```

## Passo 5 — Configurar o cliente com a URL pública

```bash
python scripts/configure_api_url.py --api-url "https://SEU-SERVICO.onrender.com"
```

Esse comando cria/atualiza `pokepy_client.json` com backend online.

## Passo 6 — Testar o jogo contra a API hospedada

Windows:

```powershell
.\scriptsun_game_online.ps1 -ApiUrl "https://SEU-SERVICO.onrender.com"
```

Linux/macOS:

```bash
./scripts/run_game_online.sh "https://SEU-SERVICO.onrender.com"
```

## Observações do plano gratuito

Serviços gratuitos podem dormir após período de inatividade. Na primeira requisição após pausa, a API pode demorar mais para responder. O cliente usa timeout e fallback local para preservar a experiência durante testes.
