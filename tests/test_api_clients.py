from __future__ import annotations

from typing import Any

import pytest
from PokePY.infrastructure.api_multiplayer_gateway import ApiMultiplayerGateway
from PokePY.infrastructure.http.json_client import HttpJsonClient
from PokePY.services.multiplayer_contracts import PlayerSnapshot, PokemonSnapshot


class FakeResponse:
    def __init__(self, payload: object, status_code: int = 200):
        self._payload = payload
        self.status_code = status_code
        self.content = b"{}"
        self.text = "{}"

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            import requests

            raise requests.HTTPError(f"HTTP {self.status_code}")

    def json(self) -> object:
        return self._payload


def test_http_json_client_builds_hosted_url(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}

    def fake_request(method: str, url: str, **kwargs: Any) -> FakeResponse:
        captured.update(method=method, url=url, kwargs=kwargs)
        return FakeResponse({"status": "ok"})

    monkeypatch.setattr("requests.request", fake_request)
    client = HttpJsonClient("https://pokepygame.onrender.com/", 65)

    assert client.get("/health") == {"status": "ok"}
    assert captured["url"] == "https://pokepygame.onrender.com/health"
    assert captured["kwargs"]["timeout"] == 65


def test_http_json_client_allows_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("requests.request", lambda *args, **kwargs: FakeResponse({}, 404))
    client = HttpJsonClient("https://pokepygame.onrender.com", 65)

    assert client.request("GET", "/missing", allow_not_found=True) is None


def test_multiplayer_gateway_uses_http_client_contract(monkeypatch: pytest.MonkeyPatch) -> None:
    client = HttpJsonClient("https://pokepygame.onrender.com", 65)
    payload = {
        "ticket_id": "ticket-1",
        "player_id": "session-1",
        "status": "waiting",
        "match_id": None,
    }

    def fake_request(*args: Any, **kwargs: Any) -> dict[str, Any]:
        return payload

    monkeypatch.setattr(client, "request", fake_request)
    gateway = ApiMultiplayerGateway(client)
    pokemon = PokemonSnapshot("Pikachu", "Elétrico", 1, 100, 100, 0, ("Choque",), 1)
    player = PlayerSnapshot("session-1", "MesmoNome", (pokemon,))

    ticket = gateway.enter_queue(player)

    assert ticket.player_id == "session-1"
    assert ticket.ticket_id == "ticket-1"
