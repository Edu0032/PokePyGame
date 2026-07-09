# PokePY

Jogo 2D em Python com cliente Pygame, API REST em FastAPI, persistência relacional e multiplayer por matchmaking.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-REST-green)
![Pygame](https://img.shields.io/badge/Pygame-client-orange)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![Pytest](https://img.shields.io/badge/tests-pytest-blueviolet)
![Docker](https://img.shields.io/badge/Docker-ready-blue)
![Render](https://img.shields.io/badge/Render-deployable-black)

## Visão geral

PokePY é um projeto educacional de desenvolvimento de software com duas partes principais:

- **Cliente do jogo**: aplicação desktop em Python/Pygame, com exploração, batalhas, inventário, seleção de time, ranking e tela multiplayer.
- **Backend**: API REST em FastAPI responsável por ranking, progresso do jogador, matchmaking e sincronização de ações multiplayer.

O cliente não acessa o banco de dados diretamente. Em modo online, ele envia requisições HTTP para a API. A API valida as regras, grava os dados e devolve o estado atualizado ao cliente.

> Projeto fan-made para fins educacionais. Os assets podem ser substituídos por recursos autorais em uma distribuição comercial.

## O que o projeto demonstra

| Área | Demonstração prática |
| --- | --- |
| Python | POO, dataclasses, enums, type hints, organização em pacotes e serviços |
| Game dev | Loop Pygame, telas, sprites, mapa, colisão, batalha e inventário |
| Arquitetura | State Machine, camadas de domínio, serviços, infraestrutura e UI |
| Backend | FastAPI, rotas REST, schemas Pydantic, tratamento de erros e OpenAPI |
| Banco de dados | SQLAlchemy, repositórios, migrações Alembic, MySQL local e PostgreSQL no Render |
| Multiplayer | Fila de matchmaking, sessão de partida, turno, validação de ações e histórico |
| Distribuição | Build com PyInstaller e configuração de API hospedada |
| Qualidade | Pytest, CI no GitHub Actions, Docker Compose e documentação técnica |

## Fluxo online na prática

```mermaid
sequenceDiagram
    participant Player1 as Cliente P1
    participant Player2 as Cliente P2
    participant API as FastAPI / Render
    participant DB as Banco relacional

    Player1->>API: Entra na fila multiplayer
    API->>DB: Cria ticket P1
    Player2->>API: Entra na fila multiplayer
    API->>DB: Cria ticket P2 e partida
    API-->>Player1: Retorna match_id
    API-->>Player2: Retorna match_id
    Player1->>API: Envia ação de ataque
    API->>API: Valida turno e aplica regra
    API->>DB: Salva snapshot e histórico
    Player2->>API: Consulta estado atualizado
    API-->>Player2: Retorna HP, turno e ações
```

## Banco de dados e API

A API persiste três tipos principais de informação:

1. **Ranking**: menor tempo para concluir o jogo.
2. **Progresso do jogador**: nome, zona, posição, itens e time atual.
3. **Multiplayer**: tickets de fila, partidas e ações executadas.

Endpoints principais:

| Método | Rota | Função |
| --- | --- | --- |
| `GET` | `/health` | Verifica se a API está online |
| `GET` | `/health/ready` | Verifica se API e banco estão prontos |
| `GET` | `/leaderboard` | Lista os melhores tempos |
| `POST` | `/leaderboard` | Registra uma vitória no ranking |
| `PUT` | `/players/{player_id}/progress` | Salva progresso do jogador |
| `GET` | `/players/{player_id}/progress` | Lê progresso salvo |
| `POST` | `/multiplayer/matchmaking/join` | Entra na fila multiplayer |
| `GET` | `/multiplayer/matchmaking/status/{ticket_id}` | Consulta status da fila |
| `GET` | `/multiplayer/matches/{match_id}` | Lê estado da partida |
| `POST` | `/multiplayer/matches/{match_id}/actions` | Envia ataque, cura, troca ou saída |

Documentação detalhada: [`PokePY/docs/API_DATABASE_MULTIPLAYER.md`](PokePY/docs/API_DATABASE_MULTIPLAYER.md).

## Estrutura do repositório

```text
PokePY/
  api/                 Aplicação FastAPI, rotas, schemas e dependências
  data/                Catálogos estáticos do jogo
  distribution/        Leitura de configuração para código-fonte e executável
  domain/              Entidades, sessão e modelos de domínio
  game/                State machine e estados do jogo
  infrastructure/      Repositórios JSON, HTTP, SQLAlchemy e assets
  services/            Regras de negócio, ranking, progresso e multiplayer
  ui/                  Telas e componentes Pygame
  sprites/             Imagens do jogo
  backgrounds/         Fundos de batalha
  mapa/                Mapas e máscaras de colisão
migrations/            Migrações Alembic
scripts/               Execução, testes, deploy e build de executável
packaging/             Exemplos de configuração do cliente
PokePY/docs/           Documentação técnica objetiva
```

## Rodar localmente como desenvolvedor

```bash
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Linux/macOS:
# source .venv/bin/activate

pip install -r requirements-dev.txt
python -m PokePY.main
```

Por padrão, o jogo roda com arquivos JSON locais. Isso permite testar o cliente sem API e sem banco.

## Rodar API local com MySQL

```bash
docker compose up --build
```

Depois acesse:

```text
http://127.0.0.1:8000/docs
```

Rodar o cliente conectado à API local:

```powershell
.\scriptsun_game_online.ps1 -ApiUrl "http://127.0.0.1:8000"
```

Linux/macOS:

```bash
./scripts/run_game_online.sh "http://127.0.0.1:8000"
```

## Deploy da API no Render

O repositório inclui `render.yaml`, que cria:

- um serviço web FastAPI;
- um banco PostgreSQL gerenciado;
- variáveis de ambiente;
- comando de migração Alembic;
- health check.

Guia completo: [`PokePY/docs/RENDER_DEPLOY_PTBR.md`](PokePY/docs/RENDER_DEPLOY_PTBR.md).

## Configurar o cliente com a API hospedada

Depois que a API estiver no Render, use a URL pública no cliente:

```bash
python scripts/configure_api_url.py --api-url "https://SEU-SERVICO.onrender.com"
```

Para rodar pelo código-fonte:

```powershell
.\scriptsun_game_online.ps1 -ApiUrl "https://SEU-SERVICO.onrender.com"
```

Para gerar executável já apontando para a API hospedada:

```bash
pip install -r requirements-build.txt
python scripts/build_executable.py --api-url "https://SEU-SERVICO.onrender.com"
```

Guia completo: [`PokePY/docs/EXECUTABLE_PTBR.md`](PokePY/docs/EXECUTABLE_PTBR.md).

## Testes

```bash
pip install -r requirements-dev.txt
pytest
```

Com cobertura:

```bash
pytest --cov=PokePY --cov-report=term-missing
```

## Publicação no GitHub

Guia prático: [`PokePY/docs/GITHUB_SETUP_PTBR.md`](PokePY/docs/GITHUB_SETUP_PTBR.md).

## Resumo para currículo

**PokePY — jogo 2D com API REST, banco de dados e multiplayer**  
Projeto educacional em Python com Pygame, FastAPI, SQLAlchemy, MySQL/PostgreSQL, Docker e Pytest. Inclui arquitetura em camadas, state machine, ranking persistente, progresso do jogador, matchmaking multiplayer, API REST documentada e build de executável com PyInstaller.
