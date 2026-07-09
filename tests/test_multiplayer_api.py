
def test_matchmaking_pairs_two_players(api_client, multiplayer_player_payload):
    first = api_client.post("/multiplayer/matchmaking/join", json={"player": multiplayer_player_payload("p1", "Ana")})
    assert first.status_code == 201
    assert first.json()["status"] == "waiting"
    second = api_client.post("/multiplayer/matchmaking/join", json={"player": multiplayer_player_payload("p2", "Bruno")})
    assert second.status_code == 201
    assert second.json()["status"] == "ready"
    assert second.json()["match_id"] is not None
    status = api_client.get(f"/multiplayer/matchmaking/status/{first.json()['ticket_id']}")
    assert status.json()["status"] == "ready"
    assert status.json()["match_id"] == second.json()["match_id"]


def test_multiplayer_action_changes_turn_and_hp(api_client, multiplayer_player_payload):
    api_client.post("/multiplayer/matchmaking/join", json={"player": multiplayer_player_payload("p1", "Ana")})
    ticket = api_client.post("/multiplayer/matchmaking/join", json={"player": multiplayer_player_payload("p2", "Bruno")}).json()
    match = api_client.get(f"/multiplayer/matches/{ticket['match_id']}").json()
    active_player_id = match["active_player_id"]
    response = api_client.post(
        f"/multiplayer/matches/{ticket['match_id']}/actions",
        json={"player_id": active_player_id, "action_type": "attack", "payload": {"attack_index": 0}},
    )
    assert response.status_code == 200
    updated = response.json()["match"]
    assert updated["active_player_id"] != active_player_id
    damaged_player = next(player for player in updated["players"] if player["player_id"] != active_player_id)
    assert damaged_player["team"][0]["hp"] < 100


def test_rejects_action_outside_player_turn(api_client, multiplayer_player_payload):
    api_client.post("/multiplayer/matchmaking/join", json={"player": multiplayer_player_payload("p1", "Ana")})
    ticket = api_client.post("/multiplayer/matchmaking/join", json={"player": multiplayer_player_payload("p2", "Bruno")}).json()
    match = api_client.get(f"/multiplayer/matches/{ticket['match_id']}").json()
    inactive_player_id = next(player["player_id"] for player in match["players"] if player["player_id"] != match["active_player_id"])
    response = api_client.post(
        f"/multiplayer/matches/{ticket['match_id']}/actions",
        json={"player_id": inactive_player_id, "action_type": "attack", "payload": {"attack_index": 0}},
    )
    assert response.status_code == 409


def test_repeated_action_id_is_idempotent(api_client, multiplayer_player_payload):
    api_client.post("/multiplayer/matchmaking/join", json={"player": multiplayer_player_payload("p1", "Ana")})
    ticket = api_client.post("/multiplayer/matchmaking/join", json={"player": multiplayer_player_payload("p2", "Bruno")}).json()
    match = api_client.get(f"/multiplayer/matches/{ticket['match_id']}").json()
    action_payload = {
        "player_id": match["active_player_id"],
        "action_type": "attack",
        "payload": {"attack_index": 0},
        "action_id": "fixed-action-id",
    }
    first = api_client.post(f"/multiplayer/matches/{ticket['match_id']}/actions", json=action_payload)
    second = api_client.post(f"/multiplayer/matches/{ticket['match_id']}/actions", json=action_payload)
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["match"] == second.json()["match"]
