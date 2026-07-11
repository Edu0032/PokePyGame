from __future__ import annotations

import random
from dataclasses import replace

from PokePY.config import BATTLE_CONFIG
from PokePY.services.combat_rules import special_attack_damage
from PokePY.services.multiplayer_contracts import (
    MatchSnapshot,
    MatchStatus,
    MultiplayerAction,
    MultiplayerActionType,
    PlayerSnapshot,
    PokemonSnapshot,
)
from PokePY.services.multiplayer_errors import InvalidActionError, PlayerNotInMatchError


class MultiplayerBattleRules:
    def __init__(self, rng: random.Random | None = None):
        self.rng = rng or random.Random()

    def apply_action(
        self,
        match: MatchSnapshot,
        action: MultiplayerAction,
    ) -> MatchSnapshot:
        players = list(match.players)
        player_index = self.player_index(match, action.player_id)
        opponent_index = 1 - player_index
        actor = players[player_index]
        opponent = players[opponent_index]
        events = list(match.events[-8:])

        if action.action_type == MultiplayerActionType.ATTACK:
            actor, opponent, new_events = self.apply_attack(
                actor,
                opponent,
                int(action.payload.get("attack_index", 0)),
            )
            events.extend(new_events)
        elif action.action_type == MultiplayerActionType.SWITCH:
            actor, new_events = self.apply_switch(
                actor,
                int(action.payload.get("pokemon_index", -1)),
            )
            events.extend(new_events)
        elif action.action_type == MultiplayerActionType.HEAL:
            actor, new_events = self.apply_heal(actor)
            events.extend(new_events)
        elif action.action_type == MultiplayerActionType.FLEE:
            events.append(f"{actor.player_name} desistiu da batalha.")
            players[player_index] = actor
            players[opponent_index] = opponent
            return replace(
                match,
                status=MatchStatus.FINISHED,
                players=tuple(players),
                active_player_id=None,
                winner_player_id=opponent.player_id,
                events=tuple(events[-10:]),
            )
        else:
            raise InvalidActionError("Ação multiplayer desconhecida.")

        players[player_index] = actor
        players[opponent_index] = opponent
        winner = self.winner(tuple(players))
        if winner:
            events.append(f"{winner.player_name} venceu a batalha online!")

        return replace(
            match,
            status=MatchStatus.FINISHED if winner else MatchStatus.RUNNING,
            players=tuple(players),
            active_player_id=None if winner else opponent.player_id,
            winner_player_id=winner.player_id if winner else None,
            turn_number=match.turn_number + 1,
            events=tuple(events[-10:]),
        )

    def apply_attack(
        self,
        actor: PlayerSnapshot,
        opponent: PlayerSnapshot,
        attack_index: int,
    ) -> tuple[PlayerSnapshot, PlayerSnapshot, list[str]]:
        attacker = self.active_pokemon(actor)
        defender = self.active_pokemon(opponent)
        if attacker is None or defender is None:
            raise InvalidActionError("Pokémon ativo ausente.")

        wants_special = attack_index > 0
        required = BATTLE_CONFIG.special_charge_required
        if wants_special and actor.normal_attack_count < required:
            raise InvalidActionError("O ataque especial ainda não está carregado.")
        if not wants_special and actor.normal_attack_count >= required:
            raise InvalidActionError("O ataque especial está pronto e deve ser utilizado.")

        if wants_special:
            base_damage = (
                self.rng.randint(
                    BATTLE_CONFIG.special_damage_min,
                    BATTLE_CONFIG.special_damage_max,
                )
                + max(0, attacker.level - 1) * 2
            )
            damage = special_attack_damage(base_damage)
            attack_name = "Ataque Especial"
            updated_actor = replace(actor, normal_attack_count=0)
        else:
            damage = (
                self.rng.randint(
                    BATTLE_CONFIG.basic_damage_min,
                    BATTLE_CONFIG.basic_damage_max,
                )
                + max(0, attacker.level - 1) * 2
            )
            attack_name = "Ataque Básico"
            updated_actor = replace(
                actor,
                normal_attack_count=min(required, actor.normal_attack_count + 1),
            )

        defender_team = list(opponent.team)
        damaged_defender = replace(defender, hp=max(0, defender.hp - damage))
        defender_team[opponent.active_pokemon_index] = damaged_defender
        events = [f"{actor.player_name}: {attacker.name} usou {attack_name} e causou {damage} de dano."]

        new_active_index = opponent.active_pokemon_index
        if damaged_defender.hp <= 0:
            events.append(f"{damaged_defender.name} desmaiou.")
            new_active_index = self.first_alive_index(defender_team)
            if new_active_index >= 0:
                events.append(f"{opponent.player_name} enviou {defender_team[new_active_index].name}.")
            else:
                new_active_index = opponent.active_pokemon_index

        updated_opponent = replace(
            opponent,
            team=tuple(defender_team),
            active_pokemon_index=new_active_index,
        )
        return updated_actor, updated_opponent, events

    def apply_switch(
        self,
        actor: PlayerSnapshot,
        pokemon_index: int,
    ) -> tuple[PlayerSnapshot, list[str]]:
        if pokemon_index < 0 or pokemon_index >= len(actor.team):
            raise InvalidActionError("Troca inválida.")
        selected = actor.team[pokemon_index]
        if selected.hp <= 0:
            raise InvalidActionError(f"{selected.name} não pode batalhar.")
        if pokemon_index == actor.active_pokemon_index:
            raise InvalidActionError(f"{selected.name} já está em batalha.")
        return (
            replace(actor, active_pokemon_index=pokemon_index),
            [f"{actor.player_name} trocou para {selected.name}."],
        )

    def apply_heal(self, actor: PlayerSnapshot) -> tuple[PlayerSnapshot, list[str]]:
        potions = actor.items.get("Poção", 0)
        pokemon = self.active_pokemon(actor)
        if potions <= 0 or pokemon is None:
            raise InvalidActionError("A cura falhou: sem poções.")
        if pokemon.hp >= pokemon.max_hp:
            raise InvalidActionError(f"{pokemon.name} já está com o HP máximo.")

        team = list(actor.team)
        healed = replace(
            pokemon,
            hp=min(pokemon.max_hp, pokemon.hp + BATTLE_CONFIG.potion_heal),
        )
        team[actor.active_pokemon_index] = healed
        items = actor.items.copy()
        items["Poção"] = potions - 1
        return (
            replace(actor, team=tuple(team), items=items),
            [f"{actor.player_name} curou {pokemon.name}."],
        )

    def winner(self, players: tuple[PlayerSnapshot, ...]) -> PlayerSnapshot | None:
        alive = [player for player in players if any(pokemon.hp > 0 for pokemon in player.team)]
        return alive[0] if len(alive) == 1 else None

    def player_index(self, match: MatchSnapshot, player_id: str) -> int:
        for index, player in enumerate(match.players):
            if player.player_id == player_id:
                return index
        raise PlayerNotInMatchError("Jogador não pertence a esta partida.")

    def opponent(
        self,
        match: MatchSnapshot,
        player_id: str,
    ) -> PlayerSnapshot | None:
        return next(
            (player for player in match.players if player.player_id != player_id),
            None,
        )

    def player_name(self, match: MatchSnapshot, player_id: str) -> str:
        return next(
            (player.player_name for player in match.players if player.player_id == player_id),
            "Jogador",
        )

    def active_pokemon(self, player: PlayerSnapshot) -> PokemonSnapshot | None:
        if not player.team:
            return None
        index = max(0, min(player.active_pokemon_index, len(player.team) - 1))
        return player.team[index]

    def first_alive_index(self, team: list[PokemonSnapshot]) -> int:
        for index, pokemon in enumerate(team):
            if pokemon.hp > 0:
                return index
        return -1

    def append_event(self, match: MatchSnapshot, event: str) -> tuple[str, ...]:
        return tuple(list(match.events[-9:]) + [event])
