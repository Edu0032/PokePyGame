# Guia de estudo técnico do PokePY

Este guia explica as tecnologias, técnicas e conceitos usados no PokePY. A organização segue a estrutura real do projeto para facilitar estudo, revisão e preparação para entrevistas.

## 1. Python aplicado ao projeto

### 1.1 Módulos e pacotes

O projeto é dividido em pacotes como `domain`, `services`, `infrastructure`, `ui`, `game` e `api`. Essa divisão evita arquivos muito grandes e facilita manutenção.

Aplicação:

```text
PokePY/domain        -> modelos centrais
PokePY/services      -> regras de negócio
PokePY/infrastructure -> banco, JSON, HTTP e assets
PokePY/ui            -> telas Pygame
PokePY/api           -> backend FastAPI
```

Estudo recomendado:

- Como funciona `__init__.py`.
- Diferença entre módulo e pacote.
- Imports absolutos e relativos.
- Organização por responsabilidade.

### 1.2 Programação orientada a objetos

O projeto usa classes para representar entidades, serviços, repositórios e views.

Conceitos aplicados:

- Classe.
- Objeto.
- Encapsulamento.
- Composição.
- Separação de responsabilidade.
- Baixo acoplamento.

Exemplo de aplicação:

```text
BattleEngine aplica regra de batalha.
BattleView desenha a batalha.
BattleState coordena eventos da tela de batalha.
```

### 1.3 Type hints

Type hints deixam claro o tipo esperado por funções e métodos.

Exemplo:

```python
def read_match(self, match_id: str) -> MatchSnapshot | None:
    ...
```

O que estudar:

- `str`, `int`, `float`, `bool`.
- `list`, `dict`, `tuple`.
- Union com `|`.
- Tipos opcionais com `None`.
- Benefícios para manutenção e MyPy.

### 1.4 Dataclasses

Dataclasses reduzem repetição em classes usadas como estruturas de dados.

Exemplo:

```python
@dataclass(frozen=True)
class PokemonSnapshot:
    name: str
    level: int
    hp: int
```

O `frozen=True` torna o objeto imutável. Para alterar um snapshot, usa-se `replace`, criando uma nova versão do objeto.

### 1.5 Enums

Enums evitam strings soltas no código.

Exemplo:

```python
class MatchStatus(str, Enum):
    WAITING = "waiting"
    RUNNING = "running"
    FINISHED = "finished"
```

Benefícios:

- Evita erros de digitação.
- Facilita autocomplete.
- Centraliza valores possíveis.

### 1.6 Protocols

Protocols representam contratos. Uma classe não precisa herdar explicitamente do protocolo; basta ter os métodos esperados.

Exemplo de conceito:

```text
MultiplayerService depende de MultiplayerRepository.
SQLAlchemyMultiplayerRepository implementa os métodos necessários.
```

Esse padrão ajuda a trocar infraestrutura sem alterar regra de negócio.

## 2. Arquitetura do jogo

### 2.1 Game loop

Todo jogo em Pygame costuma seguir o ciclo:

```text
ler eventos -> atualizar estado -> desenhar tela -> controlar FPS
```

No PokePY, esse ciclo fica no núcleo da aplicação e delega comportamentos para a state machine.

### 2.2 State Machine

State Machine é uma técnica para controlar telas e fluxos.

Estados do projeto:

```text
PLAYER_NAME
TEAM_SELECTION
EXPLORE
INVENTORY
BATTLE
LEADERBOARD
MULTIPLAYER_LOBBY
MULTIPLAYER_BATTLE
```

Cada estado tem responsabilidade própria. Isso evita um `app.py` com todas as regras do jogo misturadas.

### 2.3 Separação entre estado, regra e tela

Um padrão importante do projeto:

```text
State -> coordena eventos
Service -> aplica regra
View -> desenha interface
```

Exemplo:

```text
MultiplayerBattleState -> coordena entrada do jogador
MultiplayerService -> aplica regra da partida
MultiplayerBattleView -> desenha a tela online
```

## 3. Arquitetura backend

### 3.1 FastAPI

FastAPI cria APIs REST com Python. O projeto usa FastAPI para expor ranking, progresso e multiplayer.

Conceitos aplicados:

- Rotas HTTP.
- Request body.
- Response model.
- Status codes.
- OpenAPI.
- Documentação interativa em `/docs`.

### 3.2 Rotas

Rotas são agrupadas por responsabilidade:

```text
routes/health.py       -> disponibilidade da API
routes/leaderboard.py  -> ranking
routes/progress.py     -> progresso do jogador
routes/multiplayer.py  -> fila e partidas online
```

### 3.3 Pydantic

Pydantic valida entrada e saída da API.

Exemplo de conceito:

```text
Payload recebido -> schema Pydantic -> dados validados -> serviço
```

Benefícios:

- Evita dados inválidos.
- Gera documentação automática.
- Facilita integração com clientes.

### 3.4 Tratamento de erros

Erros são convertidos em respostas HTTP padronizadas.

Exemplos:

```text
404 -> recurso não encontrado
409 -> conflito de regra de negócio
503 -> banco indisponível
500 -> erro inesperado
```

## 4. Banco de dados

### 4.1 MySQL

MySQL armazena ranking, progresso, tickets, partidas e ações multiplayer.

Tabelas principais:

```text
leaderboard_scores
player_progress
multiplayer_tickets
multiplayer_matches
multiplayer_actions
```

### 4.2 SQLAlchemy

SQLAlchemy é usado como ORM. Ele permite trabalhar com classes Python que representam tabelas.

O que estudar:

- Engine.
- Session.
- Modelos ORM.
- Queries.
- Transações.
- Relacionamento entre Python e SQL.

### 4.3 Alembic

Alembic controla alterações no schema do banco.

Comandos importantes:

```bash
alembic upgrade head
alembic revision --autogenerate -m "descricao_da_migration"
```

### 4.4 Repositórios

Repositórios isolam detalhes de armazenamento.

Exemplo:

```text
LeaderboardService não sabe se o ranking está em JSON, API ou MySQL.
Ele apenas chama o contrato do repositório.
```

## 5. API client e comunicação HTTP

O jogo usa clientes HTTP para conversar com a API.

Conceitos aplicados:

- GET.
- POST.
- PUT.
- JSON.
- Timeout.
- Tratamento de falha.
- Fallback local para ranking/progresso.

Exemplo de fluxo:

```text
Jogo -> ApiLeaderboardRepository -> JsonHttpClient -> FastAPI -> MySQL
```

## 6. Multiplayer

### 6.1 Matchmaking

Matchmaking é a lógica que junta dois jogadores.

Fluxo:

```text
Jogador A entra na fila -> status waiting
Jogador B entra na fila -> API cria match running
Ambos recebem match_id
```

### 6.2 Snapshot

Snapshot é uma fotografia do estado de um jogador ou partida em determinado momento.

No projeto existem:

```text
PokemonSnapshot
PlayerSnapshot
MatchSnapshot
```

Esses objetos são ideais para tráfego entre cliente e servidor.

### 6.3 Turnos

A API guarda `active_player_id`. Somente esse jogador pode agir.

Regra:

```text
player_id da ação precisa ser igual ao active_player_id da partida
```

### 6.4 Idempotência

Idempotência evita duplicidade quando uma requisição é reenviada.

Exemplo:

```text
O cliente envia action_id = abc123.
Se a conexão falha e a mesma ação é reenviada, a API reconhece abc123 e não aplica dano duas vezes.
```

### 6.5 Polling

Polling é uma consulta periódica ao servidor.

Exemplo:

```text
A cada intervalo, o cliente chama GET /multiplayer/matches/{match_id}
```

Vantagem:

- Simples de testar.
- Fácil de demonstrar.
- Funciona bem para uma primeira versão.

Evolução futura:

- WebSocket para comunicação em tempo real.

## 7. Testes

### 7.1 Pytest

Pytest executa testes automaticamente.

Comando:

```bash
pytest
```

### 7.2 Fixtures

Fixtures criam objetos usados por vários testes.

Exemplo:

```text
api_client
multiplayer_player_payload
```

### 7.3 TestClient

TestClient permite testar a API sem abrir servidor com Uvicorn.

### 7.4 SQLite em memória

Os testes usam banco em memória para velocidade e isolamento.

Benefícios:

- Testes rápidos.
- Não exige MySQL instalado.
- Estado limpo a cada execução.

### 7.5 Cobertura

Coverage mostra quais partes do código são exercitadas por testes.

Comando:

```bash
pytest --cov=PokePY --cov-report=term-missing
```

## 8. Qualidade

### 8.1 Ruff

Ruff encontra problemas de estilo, imports e simplificações.

Comando:

```bash
ruff check PokePY tests
```

### 8.2 Black

Black formata o código automaticamente.

Comando:

```bash
black PokePY tests
```

### 8.3 MyPy

MyPy verifica tipos estaticamente.

Comando:

```bash
mypy PokePY
```

### 8.4 Pre-commit

Pre-commit roda checks antes do commit.

Comandos:

```bash
pre-commit install
pre-commit run --all-files
```

## 9. Docker e ambiente

### 9.1 Dockerfile

Define como empacotar a API.

### 9.2 Docker Compose

Sobe API e MySQL juntos.

Comando:

```bash
docker compose up --build
```

### 9.3 Variáveis de ambiente

Variáveis permitem mudar comportamento sem alterar código.

Exemplos:

```text
POKEPY_DATABASE_URL
POKEPY_API_BASE_URL
POKEPY_LEADERBOARD_BACKEND
POKEPY_PROGRESS_BACKEND
```

## 10. GitHub e CI

### 10.1 GitHub Actions

A pipeline roda lint e testes automaticamente.

Arquivo:

```text
.github/workflows/ci.yml
```

### 10.2 Templates

O repositório contém templates para issues e pull requests.

Objetivo:

- Padronizar reports.
- Facilitar revisão.
- Demonstrar organização profissional.

## 11. Ordem recomendada de estudo

1. Python modular e POO.
2. Pygame e game loop.
3. State Machine.
4. Dataclasses, enums e type hints.
5. Repository Pattern e Service Layer.
6. FastAPI e Pydantic.
7. SQLAlchemy e MySQL.
8. Alembic migrations.
9. Pytest e fixtures.
10. Docker Compose.
11. GitHub Actions.
12. Multiplayer por API.
13. Idempotência e consistência de estado.
14. Evolução para WebSocket.

## 12. Perguntas de entrevista que o projeto ajuda a responder

### Por que separar services, domain e infrastructure?

Para manter regra de negócio independente de interface, banco e API. Isso facilita testes e troca de tecnologia.

### Por que usar repositórios?

Para esconder detalhes de persistência. O serviço não precisa saber se os dados estão em JSON, MySQL ou API remota.

### Por que usar FastAPI?

Pela integração com type hints, validação com Pydantic e documentação OpenAPI automática.

### Por que usar Alembic?

Para versionar alterações no banco e manter controle sobre evolução do schema.

### Por que usar polling no multiplayer?

Polling é mais simples e estável para a primeira versão. A arquitetura mantém caminho aberto para WebSocket.

### O que é idempotência?

É a propriedade de uma ação poder ser repetida sem gerar efeito duplicado. No projeto, `action_id` evita aplicar a mesma ação duas vezes.
