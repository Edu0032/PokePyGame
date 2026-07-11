from dataclasses import asdict

from PokePY.domain.models import Player, Pokemon
from PokePY.services.multiplayer_contracts import (
    MatchSnapshot,
    MatchStatus,
    MatchTicket,
    MultiplayerAction,
    MultiplayerActionType,
    PlayerSnapshot,
    PokemonSnapshot,
)


class MultiplayerSerializer:
    def pokemon_to_dict(self, pokemon: PokemonSnapshot) -> dict:
        payload = asdict(pokemon)
        payload["attacks"] = list(pokemon.attacks)
        return payload

    def pokemon_from_dict(self, payload: dict) -> PokemonSnapshot:
        return PokemonSnapshot(
            name=str(payload["name"]),
            type=str(payload["type"]),
            level=int(payload["level"]),
            hp=int(payload["hp"]),
            max_hp=int(payload["max_hp"]),
            xp=int(payload.get("xp", 0)),
            attacks=tuple(str(attack) for attack in payload.get("attacks", [])),
            evolution_stage=int(payload.get("evolution_stage", 0)),
        )

    def player_to_dict(self, player: PlayerSnapshot) -> dict:
        return {
            "player_id": player.player_id,
            "player_name": player.player_name,
            "team": [self.pokemon_to_dict(pokemon) for pokemon in player.team],
            "active_pokemon_index": player.active_pokemon_index,
            "items": {str(key): int(value) for key, value in player.items.items()},
            "normal_attack_count": int(player.normal_attack_count),
        }

    def player_from_dict(self, payload: dict) -> PlayerSnapshot:
        return PlayerSnapshot(
            player_id=str(payload["player_id"]),
            player_name=str(payload["player_name"]),
            team=tuple(self.pokemon_from_dict(pokemon) for pokemon in payload.get("team", [])),
            active_pokemon_index=int(payload.get("active_pokemon_index", 0)),
            items={str(key): int(value) for key, value in payload.get("items", {}).items()},
            normal_attack_count=int(payload.get("normal_attack_count", 0)),
        )

    def ticket_to_dict(self, ticket: MatchTicket) -> dict:
        return {
            "ticket_id": ticket.ticket_id,
            "player_id": ticket.player_id,
            "status": ticket.status.value,
            "match_id": ticket.match_id,
        }

    def ticket_from_dict(self, payload: dict) -> MatchTicket:
        return MatchTicket(
            ticket_id=str(payload["ticket_id"]),
            player_id=str(payload["player_id"]),
            status=MatchStatus(str(payload["status"])),
            match_id=payload.get("match_id"),
        )

    def action_to_dict(self, action: MultiplayerAction) -> dict:
        return {
            "action_id": action.action_id,
            "match_id": action.match_id,
            "player_id": action.player_id,
            "action_type": action.action_type.value,
            "payload": dict(action.payload),
        }

    def action_from_dict(self, payload: dict) -> MultiplayerAction:
        return MultiplayerAction(
            action_id=str(payload.get("action_id") or ""),
            match_id=str(payload["match_id"]),
            player_id=str(payload["player_id"]),
            action_type=MultiplayerActionType(str(payload["action_type"])),
            payload=dict(payload.get("payload") or {}),
        )

    def match_to_dict(self, match: MatchSnapshot) -> dict:
        return {
            "match_id": match.match_id,
            "status": match.status.value,
            "players": [self.player_to_dict(player) for player in match.players],
            "active_player_id": match.active_player_id,
            "winner_player_id": match.winner_player_id,
            "turn_number": match.turn_number,
            "events": list(match.events),
        }

    def match_from_dict(self, payload: dict) -> MatchSnapshot:
        return MatchSnapshot(
            match_id=str(payload["match_id"]),
            status=MatchStatus(str(payload["status"])),
            players=tuple(self.player_from_dict(player) for player in payload.get("players", [])),
            active_player_id=payload.get("active_player_id"),
            winner_player_id=payload.get("winner_player_id"),
            turn_number=int(payload.get("turn_number", 1)),
            events=tuple(str(event) for event in payload.get("events", [])),
        )

    def snapshot_from_player(
        self,
        player_id: str,
        player_name: str,
        player: Player,
    ) -> PlayerSnapshot:
        active_index = 0
        first_alive = player.first_alive_pokemon()
        if first_alive is not None:
            for index, pokemon in enumerate(player.team):
                if pokemon is first_alive:
                    active_index = index
                    break
        return PlayerSnapshot(
            player_id=player_id,
            player_name=player_name,
            team=tuple(PokemonSnapshot.from_pokemon(pokemon) for pokemon in player.team),
            active_pokemon_index=active_index,
            items=player.items.copy(),
            normal_attack_count=0,
        )

    def apply_snapshot_to_player(
        self,
        snapshot: PlayerSnapshot,
        player: Player,
    ) -> None:
        player.team = [
            Pokemon(
                name=pokemon.name,
                type=pokemon.type,
                level=pokemon.level,
                hp=pokemon.hp,
                max_hp=pokemon.max_hp,
                xp=pokemon.xp,
                attacks=list(pokemon.attacks),
                evolution_stage=pokemon.evolution_stage,
            )
            for pokemon in snapshot.team
        ]
        player.items = snapshot.items.copy()
