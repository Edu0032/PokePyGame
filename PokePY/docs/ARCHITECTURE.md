# Arquitetura do PokePY

## Objetivo arquitetural

O projeto separa o cliente do jogo, as regras de negócio, a persistência e a API. Essa divisão evita que telas Pygame acessem diretamente banco de dados, arquivos ou regras de backend.

## Camadas principais

```text
UI Pygame -> Game States -> Services -> Repository Contracts -> Infrastructure
FastAPI -> Routes -> Services -> SQLAlchemy Repositories -> Database
```

## Cliente do jogo

- `PokePY/main.py`: ponto de entrada.
- `PokePY/app.py`: composição das dependências do jogo.
- `PokePY/game/state_machine.py`: troca de telas/estados.
- `PokePY/game/states/`: estados como nome do jogador, seleção de time, exploração, inventário, batalha, ranking e multiplayer.
- `PokePY/ui/`: componentes visuais em Pygame.

## Serviços

Os serviços concentram regras de negócio:

- `leaderboard_service.py`: ranking e formatação de pontuações.
- `player_progress_service.py`: serialização e persistência do progresso.
- `multiplayer_service.py`: entrada em fila, envio de ação e leitura de partida.
- `multiplayer_battle_rules.py`: regras de turno, dano, cura e finalização de batalha.

## Repositórios

O cliente usa contratos para não depender de uma implementação específica:

- JSON local para modo offline/desenvolvimento.
- API REST para modo online.
- SQLAlchemy no backend para banco relacional.

## Banco de dados

- MySQL é usado no desenvolvimento local via Docker Compose.
- PostgreSQL é usado no Render, por ser a opção gerenciada padrão da plataforma.
- Alembic mantém o histórico de schema.

## Executável

O executável empacota cliente, assets e arquivo `pokepy_client.json`. Ele não inclui banco de dados. A persistência online acontece via API hospedada.
