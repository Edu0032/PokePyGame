# PokePY — guia rápido para avaliação técnica

## Leitura em 3 minutos

PokePY é um projeto educacional de software que combina jogo 2D, API REST, persistência relacional, ranking online, progresso persistente, matchmaking multiplayer, testes automatizados e empacotamento em executável.

O projeto demonstra domínio de Python aplicado em duas frentes: cliente interativo com Pygame e backend com FastAPI. O cliente pode rodar como código-fonte ou executável. O backend pode rodar localmente com Docker/MySQL ou em nuvem com Render/PostgreSQL.

## O que avaliar primeiro

| Arquivo | O que mostra |
|---|---|
| `PokePY/app.py` | Composição principal do cliente Pygame |
| `PokePY/game/state_machine.py` | Controle de fluxo por máquina de estados |
| `PokePY/game/states/` | Separação de telas e estados do jogo |
| `PokePY/services/` | Regras de negócio, contratos e multiplayer |
| `PokePY/infrastructure/` | JSON local, HTTP gateway e repositórios SQLAlchemy |
| `PokePY/api/application.py` | Composição da aplicação FastAPI |
| `PokePY/api/routes/` | Endpoints REST separados por domínio |
| `tests/` | Testes com Pytest, API TestClient e banco em memória |
| `render.yaml` | Blueprint de deploy no Render |
| `scripts/build_executable.py` | Empacotamento do cliente com PyInstaller |

## Pontos fortes

- Separação entre domínio, serviços, infraestrutura, API e interface.
- State Machine no cliente Pygame.
- Repository Pattern para alternar JSON, API e SQLAlchemy.
- API REST documentada automaticamente via OpenAPI.
- Banco relacional com SQLAlchemy e Alembic.
- Modo online com matchmaking, sessão, turnos e `action_id` idempotente.
- Fallback local em JSON para desenvolvimento e resiliência.
- Deploy cloud com Render Blueprint.
- Build de executável para distribuição a jogadores.
- Testes automatizados com Pytest.

## Como rodar rapidamente

### Testes

```bash
pip install -r requirements-dev.txt
pytest
```

### API local

```bash
docker compose up --build
```

### Cliente local

```bash
python -m PokePY.main
```

### Cliente conectado à API

```bash
export POKEPY_BACKEND_MODE=api
export POKEPY_LEADERBOARD_BACKEND=api
export POKEPY_PROGRESS_BACKEND=api
export POKEPY_API_BASE_URL=http://127.0.0.1:8000
python -m PokePY.main
```

## Decisões arquiteturais relevantes

### Cliente não acessa banco diretamente

O cliente conversa com a API por HTTP. Isso evita distribuir credenciais de banco no executável e mantém a persistência protegida no backend.

### JSON local permanece como fallback

O JSON local permite jogar offline e facilita testes de desenvolvimento. Em modo online, a API é a fonte principal para ranking e progresso.

### Polling REST no multiplayer

O multiplayer usa polling HTTP para simplificar deploy gratuito e compatibilidade com executável. A arquitetura mantém gateways e serviços separados, deixando espaço para WebSocket em versões futuras.

### Render usa PostgreSQL

O ambiente local usa MySQL via Docker. O Render usa PostgreSQL gerenciado por ser a opção integrada mais adequada para deploy gratuito com banco relacional.

## Perguntas técnicas sugeridas

- Como a State Machine evita excesso de condicionais no `app.py`?
- Por que o cliente usa contratos/repositórios em vez de chamar arquivos JSON ou HTTP diretamente?
- Como o `action_id` evita ações duplicadas no multiplayer?
- Qual a diferença entre JSON local, MySQL local e PostgreSQL em produção?
- Por que o executável não deve conter credenciais de banco?
- Como Alembic e SQLAlchemy se complementam?
- Como o projeto pode evoluir de polling REST para WebSocket?
