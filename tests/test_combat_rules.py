import random

from PokePY.domain.models import Pokemon
from PokePY.services.battle_engine import BattleEngine
from PokePY.services.combat_rules import (
    BattleChargeTracker,
    special_attack_damage,
    xp_required_for_level,
)


def test_special_requires_two_normal_attacks():
    charge = BattleChargeTracker()
    assert charge.special_ready is False
    charge.record_normal_attack()
    assert charge.special_ready is False
    charge.record_normal_attack()
    assert charge.special_ready is True


def test_special_consumption_resets_charge():
    charge = BattleChargeTracker(2)
    assert charge.consume_special_attack() is True
    assert charge.normal_attacks == 0
    assert charge.consume_special_attack() is False


def test_special_damage_has_35_percent_bonus():
    assert special_attack_damage(100) == 135


def test_xp_requirement_is_reduced_by_30_percent():
    assert xp_required_for_level(1) == 70
    assert xp_required_for_level(3) == 210


def test_battle_engine_applies_special_bonus():
    engine = BattleEngine(random.Random(0))
    attacker = Pokemon("Pikachu", "Elétrico")
    defender = Pokemon("Squirtle", "Água", hp=200, max_hp=200)
    _, damage = engine.player_attack(attacker, defender, 1)
    assert damage >= 34
    assert defender.hp == 200 - damage
