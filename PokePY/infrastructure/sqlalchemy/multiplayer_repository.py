from datetime import datetime, timezone

from sqlalchemy import select

from PokePY.infrastructure.sqlalchemy.models import MultiplayerActionRecord, MultiplayerMatchRecord, MultiplayerTicketRecord
from PokePY.services.multiplayer_contracts import MatchSnapshot, MatchStatus, MatchTicket, MultiplayerAction, PlayerSnapshot
from PokePY.services.multiplayer_serialization import MultiplayerSerializer

class SQLAlchemyMultiplayerRepository:
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self.serializer = MultiplayerSerializer()

    def find_waiting_ticket(self, excluded_player_id: str) -> MatchTicket | None:
        with self.session_factory() as session:
            record = session.execute(
                select(MultiplayerTicketRecord)
                .where(MultiplayerTicketRecord.status == MatchStatus.WAITING.value)
                .where(MultiplayerTicketRecord.player_id != excluded_player_id)
                .order_by(MultiplayerTicketRecord.created_at.asc())
                .limit(1)
            ).scalar_one_or_none()
            return self._ticket_from_record(record) if record else None

    def find_player_ticket(self, player_id: str) -> MatchTicket | None:
        with self.session_factory() as session:
            record = session.execute(
                select(MultiplayerTicketRecord)
                .where(MultiplayerTicketRecord.player_id == player_id)
                .where(MultiplayerTicketRecord.status.in_([MatchStatus.WAITING.value, MatchStatus.READY.value, MatchStatus.RUNNING.value]))
                .order_by(MultiplayerTicketRecord.updated_at.desc())
                .limit(1)
            ).scalar_one_or_none()
            return self._ticket_from_record(record) if record else None

    def save_ticket(self, ticket: MatchTicket, player: PlayerSnapshot | None = None) -> MatchTicket:
        now = self._now()
        with self.session_factory() as session:
            record = session.get(MultiplayerTicketRecord, ticket.ticket_id)
            if record is None:
                if player is None:
                    raise ValueError("Novo ticket precisa do snapshot do jogador.")
                record = MultiplayerTicketRecord(
                    ticket_id=ticket.ticket_id,
                    player_id=ticket.player_id,
                    player_snapshot=self.serializer.player_to_dict(player),
                    status=ticket.status.value,
                    match_id=ticket.match_id,
                    created_at=now,
                    updated_at=now,
                )
                session.add(record)
            else:
                record.status = ticket.status.value
                record.match_id = ticket.match_id
                record.updated_at = now
                if player is not None:
                    record.player_snapshot = self.serializer.player_to_dict(player)
            session.commit()
        return ticket

    def load_ticket(self, ticket_id: str) -> MatchTicket | None:
        with self.session_factory() as session:
            record = session.get(MultiplayerTicketRecord, ticket_id)
            return self._ticket_from_record(record) if record else None

    def load_ticket_player(self, ticket_id: str) -> PlayerSnapshot | None:
        with self.session_factory() as session:
            record = session.get(MultiplayerTicketRecord, ticket_id)
            if record is None:
                return None
            return self.serializer.player_from_dict(record.player_snapshot)

    def save_match(self, match: MatchSnapshot) -> MatchSnapshot:
        now = self._now()
        payload = self.serializer.match_to_dict(match)
        with self.session_factory() as session:
            record = session.get(MultiplayerMatchRecord, match.match_id)
            if record is None:
                record = MultiplayerMatchRecord(
                    match_id=match.match_id,
                    status=match.status.value,
                    players=payload["players"],
                    active_player_id=match.active_player_id,
                    winner_player_id=match.winner_player_id,
                    turn_number=match.turn_number,
                    events=payload["events"],
                    created_at=now,
                    updated_at=now,
                )
                session.add(record)
            else:
                record.status = match.status.value
                record.players = payload["players"]
                record.active_player_id = match.active_player_id
                record.winner_player_id = match.winner_player_id
                record.turn_number = match.turn_number
                record.events = payload["events"]
                record.updated_at = now
            session.commit()
        return match

    def load_match(self, match_id: str) -> MatchSnapshot | None:
        with self.session_factory() as session:
            record = session.get(MultiplayerMatchRecord, match_id)
            if record is None:
                return None
            return self.serializer.match_from_dict(
                {
                    "match_id": record.match_id,
                    "status": record.status,
                    "players": record.players,
                    "active_player_id": record.active_player_id,
                    "winner_player_id": record.winner_player_id,
                    "turn_number": record.turn_number,
                    "events": record.events,
                }
            )

    def action_exists(self, action_id: str) -> bool:
        with self.session_factory() as session:
            return session.get(MultiplayerActionRecord, action_id) is not None

    def save_action(self, action: MultiplayerAction) -> None:
        payload = self.serializer.action_to_dict(action)
        with self.session_factory() as session:
            session.add(
                MultiplayerActionRecord(
                    action_id=action.action_id,
                    match_id=action.match_id,
                    player_id=action.player_id,
                    action_type=action.action_type.value,
                    payload=payload["payload"],
                    created_at=self._now(),
                )
            )
            session.commit()

    def _ticket_from_record(self, record: MultiplayerTicketRecord) -> MatchTicket:
        return MatchTicket(
            ticket_id=record.ticket_id,
            player_id=record.player_id,
            status=MatchStatus(record.status),
            match_id=record.match_id,
        )

    def _now(self) -> datetime:
        return datetime.now(timezone.utc)
