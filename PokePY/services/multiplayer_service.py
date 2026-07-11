from __future__ import annotations

import random
import threading
from dataclasses import replace
from typing import Protocol
from uuid import uuid4

from PokePY.services.multiplayer_battle_rules import MultiplayerBattleRules
from PokePY.services.multiplayer_contracts import (
    MatchSnapshot,
    MatchStatus,
    MatchTicket,
    MultiplayerAction,
    PlayerSnapshot,
)
from PokePY.services.multiplayer_errors import (
    InvalidTurnError,
    MatchNotFoundError,
    PlayerNotInMatchError,
    TicketNotFoundError,
)


class MultiplayerRepository(Protocol):
    def expire_stale_waiting_tickets(self, older_than_seconds: int) -> int: ...

    def find_waiting_ticket(self, excluded_player_id: str) -> MatchTicket | None: ...

    def find_player_ticket(self, player_id: str) -> MatchTicket | None: ...

    def save_ticket(
        self,
        ticket: MatchTicket,
        player: PlayerSnapshot | None = None,
    ) -> MatchTicket: ...

    def load_ticket(self, ticket_id: str) -> MatchTicket | None: ...

    def load_ticket_player(self, ticket_id: str) -> PlayerSnapshot | None: ...

    def save_match(self, match: MatchSnapshot) -> MatchSnapshot: ...

    def load_match(self, match_id: str) -> MatchSnapshot | None: ...

    def action_exists(self, action_id: str) -> bool: ...

    def save_action(self, action: MultiplayerAction) -> None: ...


class MultiplayerService:
    def __init__(
        self,
        repository: MultiplayerRepository,
        rng: random.Random | None = None,
        queue_ttl_seconds: int = 60,
        queue_lock: threading.RLock | None = None,
    ):
        self.repository = repository
        self.rules = MultiplayerBattleRules(rng)
        self.queue_ttl_seconds = max(30, queue_ttl_seconds)
        self._queue_lock = queue_lock or threading.RLock()

    def enter_queue(self, player: PlayerSnapshot) -> MatchTicket:
        with self._queue_lock:
            self.repository.expire_stale_waiting_tickets(self.queue_ttl_seconds)
            return self._enter_queue_locked(player)

    def _enter_queue_locked(self, player: PlayerSnapshot) -> MatchTicket:
        existing = self.repository.find_player_ticket(player.player_id)
        if existing and existing.status == MatchStatus.WAITING:
            self.repository.save_ticket(existing, player)
            return existing
        if existing and existing.match_id:
            existing_match = self.repository.load_match(existing.match_id)
            if existing_match and existing_match.status not in {
                MatchStatus.FINISHED,
                MatchStatus.CANCELED,
            }:
                return existing

        waiting_ticket = self.repository.find_waiting_ticket(player.player_id)
        own_ticket = MatchTicket(uuid4().hex, player.player_id, MatchStatus.WAITING)
        self.repository.save_ticket(own_ticket, player)
        if waiting_ticket is None:
            return own_ticket
        waiting_player = self.repository.load_ticket_player(waiting_ticket.ticket_id)
        if waiting_player is None:
            return own_ticket

        match = self._create_match(waiting_player, player)
        self.repository.save_match(match)
        ready_waiting = replace(
            waiting_ticket,
            status=MatchStatus.READY,
            match_id=match.match_id,
        )
        ready_own = replace(
            own_ticket,
            status=MatchStatus.READY,
            match_id=match.match_id,
        )
        self.repository.save_ticket(ready_waiting, waiting_player)
        self.repository.save_ticket(ready_own, player)
        return ready_own

    def ticket_status(self, ticket_id: str) -> MatchTicket | None:
        ticket = self.repository.load_ticket(ticket_id)
        if ticket is not None and ticket.status == MatchStatus.WAITING:
            self.repository.save_ticket(ticket)
        return ticket

    def cancel_queue(self, ticket_id: str, player_id: str) -> MatchTicket:
        ticket = self.repository.load_ticket(ticket_id)
        if ticket is None:
            raise TicketNotFoundError("Ticket não encontrado.")
        if ticket.player_id != player_id:
            raise PlayerNotInMatchError("O ticket pertence a outro jogador.")
        if ticket.status != MatchStatus.WAITING:
            return ticket
        return self.repository.save_ticket(replace(ticket, status=MatchStatus.CANCELED))

    def read_match(self, match_id: str) -> MatchSnapshot | None:
        return self.repository.load_match(match_id)

    def leave_match(self, match_id: str, player_id: str) -> MatchSnapshot:
        match = self._load_required_match(match_id)
        if match.status == MatchStatus.FINISHED:
            return match
        opponent = self.rules.opponent(match, player_id)
        if opponent is None:
            raise PlayerNotInMatchError("Jogador não pertence a esta partida.")
        updated = replace(
            match,
            status=MatchStatus.FINISHED,
            active_player_id=None,
            winner_player_id=opponent.player_id,
            events=self.rules.append_event(
                match,
                f"{self.rules.player_name(match, player_id)} saiu da batalha.",
            ),
        )
        return self.repository.save_match(updated)

    def send_action(self, action: MultiplayerAction) -> MatchSnapshot:
        match = self._load_required_match(action.match_id)
        if match.status == MatchStatus.FINISHED:
            return match
        if self.repository.action_exists(action.action_id):
            return match
        if action.player_id != match.active_player_id:
            raise InvalidTurnError("Ainda não é a vez desse jogador.")
        updated = self.rules.apply_action(match, action)
        self.repository.save_action(action)
        return self.repository.save_match(updated)

    def _create_match(
        self,
        waiting_player: PlayerSnapshot,
        challenger: PlayerSnapshot,
    ) -> MatchSnapshot:
        return MatchSnapshot(
            match_id=uuid4().hex,
            status=MatchStatus.RUNNING,
            players=(waiting_player, challenger),
            active_player_id=waiting_player.player_id,
            turn_number=1,
            events=(f"{waiting_player.player_name} encontrou {challenger.player_name}. A batalha começou!",),
        )

    def _load_required_match(self, match_id: str) -> MatchSnapshot:
        match = self.repository.load_match(match_id)
        if match is None:
            raise MatchNotFoundError("Partida não encontrada.")
        return match
