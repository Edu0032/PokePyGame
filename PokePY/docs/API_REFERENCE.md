# API Reference

## Base URL

Local development:

```text
http://127.0.0.1:8000
```

Hosted deployment:

```text
https://sua-api.onrender.com
```

Interactive documentation:

```text
/docs
```

## Health

### `GET /health`

Basic service check.

Response:

```json
{
  "status": "ok",
  "database": "configured"
}
```

### `GET /health/ready`

Database readiness check.

Response:

```json
{
  "status": "ok",
  "database": "ready"
}
```

## Leaderboard

### `POST /leaderboard`

Saves a completed run time.

Request:

```json
{
  "player_name": "Ana",
  "elapsed_seconds": 842
}
```

Response:

```json
{
  "entry": {
    "player_name": "Ana",
    "elapsed_seconds": 842,
    "created_at": "2026-07-09T00:00:00Z"
  },
  "position": 1
}
```

### `GET /leaderboard?limit=10`

Returns best completion times.

Response:

```json
[
  {
    "player_name": "Ana",
    "elapsed_seconds": 842,
    "created_at": "2026-07-09T00:00:00Z"
  }
]
```

### `GET /leaderboard/page?limit=10&offset=0`

Returns a paginated leaderboard page.

Response:

```json
{
  "items": [
    {
      "player_name": "Ana",
      "elapsed_seconds": 842,
      "created_at": "2026-07-09T00:00:00Z"
    }
  ],
  "limit": 10,
  "offset": 0,
  "returned": 1
}
```

## Player progress

### `PUT /players/{player_id}/progress`

Saves player progress.

Request body shape:

```json
{
  "player_id": "player-123",
  "player_name": "Ana",
  "zone_index": 1,
  "x": 120,
  "y": 320,
  "items": {
    "Poção": 3,
    "Repelente": 1
  },
  "team": []
}
```

Response:

```json
{
  "saved": true,
  "progress": {
    "player_id": "player-123",
    "player_name": "Ana",
    "zone_index": 1,
    "x": 120,
    "y": 320,
    "items": {
      "Poção": 3,
      "Repelente": 1
    },
    "team": []
  }
}
```

### `GET /players/{player_id}/progress`

Loads player progress.

Response:

```json
{
  "player_id": "player-123",
  "player_name": "Ana",
  "zone_index": 1,
  "x": 120,
  "y": 320,
  "items": {
    "Poção": 3,
    "Repelente": 1
  },
  "team": []
}
```

## Multiplayer

### `GET /multiplayer/capabilities`

Returns supported multiplayer contracts and endpoints.

### `POST /multiplayer/matchmaking/join`

Places a player in the matchmaking queue.

Request body shape:

```json
{
  "player": {
    "player_id": "p1",
    "player_name": "Player 1",
    "items": {
      "Poção": 2
    },
    "team": []
  }
}
```

Response:

```json
{
  "ticket_id": "ticket-id",
  "player_id": "p1",
  "status": "waiting",
  "match_id": null
}
```

### `GET /multiplayer/matchmaking/status/{ticket_id}`

Polls a matchmaking ticket.

Response when matched:

```json
{
  "ticket_id": "ticket-id",
  "player_id": "p1",
  "status": "matched",
  "match_id": "match-id"
}
```

### `GET /multiplayer/matches/{match_id}`

Reads a match snapshot.

### `POST /multiplayer/matches/{match_id}/actions`

Submits an action to a match.

Request:

```json
{
  "player_id": "p1",
  "action_type": "basic_attack",
  "payload": {},
  "action_id": "unique-client-action-id"
}
```

Supported action types:

```text
basic_attack
special_attack
use_potion
switch_pokemon
leave
```

Response:

```json
{
  "accepted": true,
  "match": {}
}
```

### `POST /multiplayer/matches/{match_id}/leave`

Leaves a match.

Request:

```json
{
  "player_id": "p1"
}
```

## Error behavior

| Status | Meaning |
|---|---|
| `400` | Invalid request data or URL/body mismatch |
| `404` | Resource not found |
| `409` | Invalid multiplayer action, wrong turn or player outside match |
| `503` | Database or persistence service unavailable |
