# Plano técnico: API, banco e multiplayer

Este documento descreve o papel da API, do banco de dados e do multiplayer na arquitetura do PokePY.

## Escopo atual

A API fornece três grupos principais de recursos:

```text
ranking
progresso do jogador
multiplayer
```

Endpoints disponíveis:

```text
GET  /health
POST /leaderboard
GET  /leaderboard
GET  /leaderboard/page
PUT  /players/{player_id}/progress
GET  /players/{player_id}/progress
GET  /multiplayer/capabilities
POST /multiplayer/matchmaking/join
GET  /multiplayer/matchmaking/status/{ticket_id}
GET  /multiplayer/matches/{match_id}
POST /multiplayer/matches/{match_id}/actions
POST /multiplayer/matches/{match_id}/leave
```

## Tabelas

```text
leaderboard_scores
player_progress
multiplayer_tickets
multiplayer_matches
multiplayer_actions
```

## Ranking

O ranking registra o menor tempo de conclusão da tentativa.

Fluxo:

```text
fim da run -> LeaderboardService -> Repository -> JSON ou API -> MySQL
```

## Progresso do jogador

O progresso preserva estado do jogador entre sessões e permite continuidade no modo multiplayer.

Dados persistidos:

```text
player_id
player_name
zona atual
posição
itens
time
nível
HP
XP
ataques
evolução
```

## Multiplayer

O multiplayer usa fila e sessão de partida.

Fluxo:

```text
join queue -> ticket waiting -> segundo jogador -> match running -> ações por turno -> match finished
```

## Evolução recomendada

| Etapa | Objetivo |
|---|---|
| WebSocket | Reduzir latência e evitar polling constante |
| Autenticação | Associar progresso a conta do jogador |
| Histórico de partidas | Exibir vitórias, derrotas e detalhes de combate |
| Observabilidade | Métricas, logs estruturados e rastreio de erros |
| Testes end-to-end | Validar fluxo completo entre dois clientes |
