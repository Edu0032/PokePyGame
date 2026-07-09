from PokePY.api.schemas import LeaderboardEntryResponse, MatchSnapshotResponse, MatchTicketResponse, MultiplayerPlayerPayload, PlayerProgressPayload
from PokePY.services.leaderboard_contracts import LeaderboardEntry
from PokePY.services.player_progress_service import PlayerProgress, PlayerProgressService

_serializer = PlayerProgressService(repository=None)

def leaderboard_response(entry: LeaderboardEntry) -> LeaderboardEntryResponse:
    return LeaderboardEntryResponse(
        player_name=entry.player_name,
        elapsed_seconds=entry.elapsed_seconds,
        created_at=entry.created_at,
    )

def progress_response(progress: PlayerProgress) -> PlayerProgressPayload:
    return PlayerProgressPayload(**_serializer.to_dict(progress))

def progress_from_payload(payload: PlayerProgressPayload) -> PlayerProgress:
    return _serializer.from_dict(payload.model_dump())


from PokePY.services.multiplayer_contracts import MatchSnapshot, MatchTicket, PlayerSnapshot
from PokePY.services.multiplayer_serialization import MultiplayerSerializer

_multiplayer_serializer = MultiplayerSerializer()

def multiplayer_player_response(player: PlayerSnapshot) -> MultiplayerPlayerPayload:
    return MultiplayerPlayerPayload(**_multiplayer_serializer.player_to_dict(player))

def multiplayer_player_from_payload(payload: MultiplayerPlayerPayload) -> PlayerSnapshot:
    return _multiplayer_serializer.player_from_dict(payload.model_dump())

def match_ticket_response(ticket: MatchTicket) -> MatchTicketResponse:
    return MatchTicketResponse(**_multiplayer_serializer.ticket_to_dict(ticket))

def match_snapshot_response(match: MatchSnapshot) -> MatchSnapshotResponse:
    return MatchSnapshotResponse(**_multiplayer_serializer.match_to_dict(match))
