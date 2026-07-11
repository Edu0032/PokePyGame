import random

from PokePY.services.multiplayer_battle_rules import MultiplayerBattleRules
from PokePY.services.multiplayer_contracts import (
    MatchSnapshot,
    MatchStatus,
    MultiplayerAction,
    MultiplayerActionType,
    PlayerSnapshot,
    PokemonSnapshot,
)
from PokePY.services.multiplayer_errors import PlayerNotInMatchError


def pokemon(name: str, hp: int = 100) -> PokemonSnapshot:
    return PokemonSnapshot(
        name=name,
        type="normal",
        level=1,
        hp=hp,
        max_hp=100,
        xp=0,
        attacks=("A", "B"),
        evolution_stage=1,
    )


def player(player_id: str, name: str, hp: int = 100) -> PlayerSnapshot:
    return PlayerSnapshot(
        player_id=player_id,
        player_name=name,
        team=(pokemon(f"{name}Mon", hp),),
        items={"Poção": 1},
    )


def match_snapshot() -> MatchSnapshot:
    return MatchSnapshot(
        match_id="match-1",
        status=MatchStatus.RUNNING,
        players=(player("p1", "Ana"), player("p2", "Bruno")),
        active_player_id="p1",
    )


def test_attack_applies_damage_and_changes_turn():
    rules = MultiplayerBattleRules(random.Random(1))
    action = MultiplayerAction("match-1", "p1", MultiplayerActionType.ATTACK, {"attack_index": 0})

    updated = rules.apply_action(match_snapshot(), action)

    opponent = next(player for player in updated.players if player.player_id == "p2")
    assert opponent.team[0].hp < 100
    assert updated.active_player_id == "p2"
    assert updated.turn_number == 2


def test_heal_consumes_potion():
    rules = MultiplayerBattleRules(random.Random(1))
    injured_match = MatchSnapshot(
        match_id="match-1",
        status=MatchStatus.RUNNING,
        players=(player("p1", "Ana", hp=40), player("p2", "Bruno")),
        active_player_id="p1",
    )
    action = MultiplayerAction("match-1", "p1", MultiplayerActionType.HEAL, {})

    updated = rules.apply_action(injured_match, action)

    actor = next(player for player in updated.players if player.player_id == "p1")
    assert actor.team[0].hp > 40
    assert actor.items["Poção"] == 0


def test_unknown_player_raises_domain_error():
    rules = MultiplayerBattleRules(random.Random(1))
    action = MultiplayerAction("match-1", "ghost", MultiplayerActionType.ATTACK, {"attack_index": 0})

    try:
        rules.apply_action(match_snapshot(), action)
    except PlayerNotInMatchError as error:
        assert "Jogador" in str(error)
    else:
        raise AssertionError("Expected PlayerNotInMatchError")


def test_two_normal_attacks_charge_special_and_special_resets_charge():
    rules = MultiplayerBattleRules(random.Random(1))
    actor = player("p1", "Ana")
    opponent = player("p2", "Bruno")
    actor, opponent, _ = rules.apply_attack(actor, opponent, 0)
    actor, opponent, _ = rules.apply_attack(actor, opponent, 0)
    assert actor.normal_attack_count == 2
    actor, _, _ = rules.apply_attack(actor, opponent, 1)
    assert actor.normal_attack_count == 0


def test_special_attack_is_rejected_before_charge():
    rules = MultiplayerBattleRules(random.Random(1))
    try:
        rules.apply_attack(
            player("p1", "Ana"),
            player("p2", "Bruno"),
            1,
        )
    except Exception as error:
        assert "carregado" in str(error)
    else:
        raise AssertionError("Expected special attack to be rejected")
