# Inventário técnico do PokePY

Este documento resume tecnologias, ferramentas, padrões e conceitos usados no projeto. A estrutura permite leitura rápida por categoria.

## 1. Linguagem e recursos de Python

| Item | Uso no projeto | Exemplo de aplicação |
|---|---|---|
| Python 3.11+ | Linguagem principal do cliente e da API | Pacotes `PokePY.game`, `PokePY.api`, `PokePY.services` |
| Type hints | Melhoria de clareza e suporte a análise estática | `def top_scores(limit: int) -> list[LeaderboardEntry]` |
| Dataclasses | Modelos simples e imutáveis de configuração/dados | `ScreenConfig`, `BattleConfig`, `RepositoryBundle` |
| Enum | Estados e tipos de ação com valores controlados | `GameState`, `MultiplayerActionType` |
| Protocol-like contracts | Desacoplamento entre serviços e infraestrutura | contratos de leaderboard, progresso e multiplayer |
| Context managers | Fechamento correto de conexões de banco | `with engine.connect()` em readiness check |

## 2. Cliente de jogo

| Item | Uso no projeto | Exemplo de aplicação |
|---|---|---|
| Pygame | Renderização, input, game loop e janelas | `Game.run()` e views em `PokePY/ui` |
| Game loop | Atualização contínua de estado e renderização | `clock.tick(SCREEN_CONFIG.fps)` |
| State Machine | Fluxo de telas sem excesso de condicionais | `PokePY/game/state_machine.py` |
| Sprites | Personagens, criaturas e elementos visuais | `PokePY/sprites` |
| Máscaras de mapa | Colisão e movimentação no mapa | `MapMaskService` |
| UI Views | Separação entre desenho e regra de negócio | `BattleView`, `LeaderboardView`, `MultiplayerLobbyView` |

## 3. Backend/API

| Item | Uso no projeto | Exemplo de aplicação |
|---|---|---|
| FastAPI | API REST para ranking, progresso e multiplayer | `PokePY/api/application.py` |
| APIRouter | Organização de endpoints por domínio | `routes/leaderboard.py`, `routes/multiplayer.py` |
| Pydantic | Validação e serialização de payloads | `PokePY/api/schemas.py` |
| OpenAPI | Documentação interativa automática | `/docs` |
| Exception handlers | Padronização de erros HTTP | `PokePY/api/errors.py` |
| CORS Middleware | Compatibilidade com clientes externos | `CORSMiddleware` em `create_app()` |
| Health check | Verificação de serviço e banco | `/health` e `/health/ready` |

## 4. Persistência

| Item | Uso no projeto | Exemplo de aplicação |
|---|---|---|
| JSON local | Fallback offline para ranking e progresso | `JsonLeaderboardRepository` |
| MySQL | Banco local com Docker Compose | `docker-compose.yml` |
| PostgreSQL | Banco gerenciado em produção no Render | `render.yaml` |
| SQLAlchemy ORM | Mapeamento objeto-relacional | `infrastructure/sqlalchemy/models.py` |
| Alembic | Migrations versionadas | `migrations/versions` |
| Repository Pattern | Troca de JSON, API e SQLAlchemy sem alterar serviços | `repository_factory.py` |
| Connection pooling | Verificação de conexões ativas | `pool_pre_ping=True` |

## 5. Multiplayer

| Item | Uso no projeto | Exemplo de aplicação |
|---|---|---|
| Matchmaking queue | Fila de jogadores aguardando partida | `POST /multiplayer/matchmaking/join` |
| Match session | Estado persistido da partida online | `MultiplayerMatchRecord` |
| Turn validation | Impede ação fora da vez | `InvalidTurnError` |
| Action history | Registro de ações executadas | `MultiplayerActionRecord` |
| Idempotência | Evita duplicação por reenvio HTTP | campo `action_id` |
| Polling HTTP | Sincronização simples entre clientes | leitura periódica de match snapshot |
| Snapshot serialization | Transporte de estado do jogador e criaturas | `multiplayer_serialization.py` |

## 6. Distribuição

| Item | Uso no projeto | Exemplo de aplicação |
|---|---|---|
| PyInstaller | Geração de executável para jogadores | `scripts/build_executable.py` |
| Bundled data | Inclusão de sprites, mapas e backgrounds | `--add-data` no build |
| Runtime config | URL da API embutida ou sobrescrita por ambiente | `pokepy_client.json` |
| User data directory | Saves fora da pasta temporária do executável | `%APPDATA%/PokePY/saves` |
| One-file build | Pacote simples para distribuição | `dist/PokePY.exe` |

## 7. DevOps e hospedagem

| Item | Uso no projeto | Exemplo de aplicação |
|---|---|---|
| Docker | Ambiente local reproduzível | `Dockerfile.api` |
| Docker Compose | API + MySQL local | `docker-compose.yml` |
| Render Blueprint | Deploy cloud declarativo | `render.yaml` |
| Procfile | Comando alternativo de start | `Procfile` |
| Environment variables | Configuração sem hardcode | `.env.example` |
| GitHub Actions | CI para testes e qualidade | `.github/workflows/ci.yml` |
| Dependabot | Atualizações automáticas de dependências | `.github/dependabot.yml` |

## 8. Testes e qualidade

| Item | Uso no projeto | Exemplo de aplicação |
|---|---|---|
| Pytest | Testes automatizados | `tests/` |
| Fixtures | Setup reutilizável de testes | `tests/conftest.py` |
| TestClient | Testes de API sem servidor real | `fastapi.testclient` |
| SQLite em memória | Testes rápidos de repositório/API | URL `sqlite://` |
| Coverage | Medição de partes testadas | `pytest --cov=PokePY` |
| Ruff | Lint e import sorting | `ruff check` |
| Black | Formatação consistente | `black --check` |
| MyPy | Verificação estática de tipos | `mypy PokePY` |
| Pre-commit | Checagens antes de commit | `.pre-commit-config.yaml` |

## 9. Padrões arquiteturais

| Padrão | Problema resolvido | Onde aparece |
|---|---|---|
| Layered Architecture | Separação entre UI, domínio, serviços e infraestrutura | estrutura de pacotes `ui`, `domain`, `services`, `infrastructure`, `api` |
| Repository Pattern | Troca de armazenamento sem alterar regras | JSON/API/SQLAlchemy repositories |
| Service Layer | Regras de negócio fora da UI e fora das rotas | `LeaderboardService`, `MultiplayerService` |
| Dependency Inversion | Camadas altas dependem de contratos, não de detalhes | factories e contratos de serviço |
| State Machine | Fluxo do jogo organizado por estados | `StateMachine` e `game/states` |
| Gateway Pattern | Cliente HTTP isolado da UI | `ApiMultiplayerGateway` |
| Serializer/Mapper | Conversão entre domínio e payloads | converters e serializers |

## 10. Exemplos de aplicação técnica

### Ranking online

1. O jogador conclui a run.
2. O cliente registra o tempo no `LeaderboardService`.
3. O repositório escolhido envia o score para a API ou salva em JSON.
4. A API valida o payload com Pydantic.
5. O repositório SQLAlchemy persiste no banco.
6. O ranking retorna ordenado por menor tempo.

### Progresso persistente

1. O cliente serializa player, zona, inventário e time.
2. O progresso é salvo no backend selecionado.
3. O jogo pode recuperar o estado usando `player_id`.
4. Em executável, a API hospedada mantém continuidade entre sessões.

### Multiplayer

1. Dois clientes entram na fila.
2. A API cria uma partida com snapshots dos jogadores.
3. Cada cliente consulta o estado da partida.
4. A ação enviada inclui `action_id`.
5. O servidor valida turno, aplica regra e salva histórico.
6. Os clientes recebem o snapshot atualizado por polling.
