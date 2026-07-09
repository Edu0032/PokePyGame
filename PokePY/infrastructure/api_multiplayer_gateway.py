from PokePY.infrastructure.http.json_client import HttpJsonClient
from PokePY.services.multiplayer_contracts import MatchSnapshot, MatchTicket, MultiplayerAction, PlayerSnapshot
from PokePY.services.multiplayer_serialization import MultiplayerSerializer

class ApiMultiplayerGateway:
    def __init__(self, client: HttpJsonClient):
        self.client = client
        self.serializer = MultiplayerSerializer()

    def enter_queue(self, player: PlayerSnapshot) -> MatchTicket:
        response = self.client.post("/multiplayer/matchmaking/join", {"player": self.serializer.player_to_dict(player)})
        return self.serializer.ticket_from_dict(response)

    def ticket_status(self, ticket_id: str) -> MatchTicket | None:
        try:
            response = self.client.get(f"/multiplayer/matchmaking/status/{ticket_id}")
        except Exception:
            return None
        return self.serializer.ticket_from_dict(response)

    def read_match(self, match_id: str) -> MatchSnapshot | None:
        try:
            response = self.client.get(f"/multiplayer/matches/{match_id}")
        except Exception:
            return None
        return self.serializer.match_from_dict(response)

    def send_action(self, action: MultiplayerAction) -> MatchSnapshot:
        response = self.client.post(
            f"/multiplayer/matches/{action.match_id}/actions",
            {
                "player_id": action.player_id,
                "action_type": action.action_type.value,
                "payload": action.payload,
                "action_id": action.action_id,
            },
        )
        return self.serializer.match_from_dict(response["match"])

    def leave_match(self, match_id: str, player_id: str) -> MatchSnapshot:
        response = self.client.post(f"/multiplayer/matches/{match_id}/leave", {"player_id": player_id})
        return self.serializer.match_from_dict(response)
