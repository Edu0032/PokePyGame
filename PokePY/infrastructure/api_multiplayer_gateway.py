from __future__ import annotations

from typing import cast

from PokePY.infrastructure.http.json_client import HttpJsonClient
from PokePY.services.multiplayer_contracts import (
    MatchSnapshot,
    MatchTicket,
    MultiplayerAction,
    PlayerSnapshot,
)
from PokePY.services.multiplayer_serialization import MultiplayerSerializer


class ApiMultiplayerGateway:
    def __init__(self, client: HttpJsonClient):
        self.client = client
        self.serializer = MultiplayerSerializer()

    def enter_queue(self, player: PlayerSnapshot) -> MatchTicket:
        response = self.client.request(
            "POST",
            "/multiplayer/matchmaking/join",
            json_body={"player": self.serializer.player_to_dict(player)},
        )
        return self.serializer.ticket_from_dict(cast(dict, response))

    def ticket_status(self, ticket_id: str) -> MatchTicket | None:
        response = self.client.request(
            "GET",
            f"/multiplayer/matchmaking/status/{ticket_id}",
            allow_not_found=True,
        )
        if response is None:
            return None
        return self.serializer.ticket_from_dict(cast(dict, response))

    def cancel_queue(self, ticket_id: str, player_id: str) -> MatchTicket:
        response = self.client.request(
            "POST",
            f"/multiplayer/matchmaking/{ticket_id}/cancel",
            json_body={"player_id": player_id},
        )
        return self.serializer.ticket_from_dict(cast(dict, response))

    def read_match(self, match_id: str) -> MatchSnapshot | None:
        response = self.client.request(
            "GET",
            f"/multiplayer/matches/{match_id}",
            allow_not_found=True,
        )
        if response is None:
            return None
        return self.serializer.match_from_dict(cast(dict, response))

    def send_action(self, action: MultiplayerAction) -> MatchSnapshot:
        response = self.client.request(
            "POST",
            f"/multiplayer/matches/{action.match_id}/actions",
            json_body={
                "player_id": action.player_id,
                "action_type": action.action_type.value,
                "payload": action.payload,
                "action_id": action.action_id,
            },
        )
        return self.serializer.match_from_dict(cast(dict, response)["match"])

    def leave_match(self, match_id: str, player_id: str) -> MatchSnapshot:
        response = self.client.request(
            "POST",
            f"/multiplayer/matches/{match_id}/leave",
            json_body={"player_id": player_id},
        )
        return self.serializer.match_from_dict(cast(dict, response))
