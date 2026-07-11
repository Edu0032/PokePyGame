from dataclasses import dataclass, field
from enum import StrEnum
from typing import Protocol
from uuid import uuid4

from PokePY.domain.models import Pokemon


class MultiplayerActionType(StrEnum):
    ATTACK = "attack"
    SWITCH = "switch"
    HEAL = "heal"
    FLEE = "flee"


class MatchStatus(StrEnum):
    WAITING = "waiting"
    READY = "ready"
    RUNNING = "running"
    FINISHED = "finished"
    CANCELED = "canceled"


@dataclass(frozen=True)
class PokemonSnapshot:
    name: str
    type: str
    level: int
    hp: int
    max_hp: int
    xp: int
    attacks: tuple[str, ...]
    evolution_stage: int

    @classmethod
    def from_pokemon(cls, pokemon: Pokemon) -> "PokemonSnapshot":
        return cls(
            name=pokemon.name,
            type=pokemon.type,
            level=pokemon.level,
            hp=pokemon.hp,
            max_hp=pokemon.max_hp or pokemon.hp,
            xp=pokemon.xp,
            attacks=tuple(pokemon.attacks),
            evolution_stage=pokemon.evolution_stage,
        )


@dataclass(frozen=True)
class PlayerSnapshot:
    player_id: str
    player_name: str
    team: tuple[PokemonSnapshot, ...]
    active_pokemon_index: int = 0
    items: dict[str, int] = field(default_factory=dict)
    normal_attack_count: int = 0


@dataclass(frozen=True)
class MultiplayerAction:
    match_id: str
    player_id: str
    action_type: MultiplayerActionType
    payload: dict
    action_id: str = field(default_factory=lambda: uuid4().hex)


@dataclass(frozen=True)
class MatchTicket:
    ticket_id: str
    player_id: str
    status: MatchStatus
    match_id: str | None = None


@dataclass(frozen=True)
class MatchSnapshot:
    match_id: str
    status: MatchStatus
    players: tuple[PlayerSnapshot, ...]
    active_player_id: str | None = None
    winner_player_id: str | None = None
    turn_number: int = 1
    events: tuple[str, ...] = ()


class MultiplayerGateway(Protocol):
    def enter_queue(self, player: PlayerSnapshot) -> MatchTicket: ...

    def ticket_status(self, ticket_id: str) -> MatchTicket | None: ...

    def cancel_queue(self, ticket_id: str, player_id: str) -> MatchTicket: ...

    def read_match(self, match_id: str) -> MatchSnapshot | None: ...

    def send_action(self, action: MultiplayerAction) -> MatchSnapshot: ...

    def leave_match(self, match_id: str, player_id: str) -> MatchSnapshot: ...
