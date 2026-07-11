from __future__ import annotations

from dataclasses import dataclass

from PokePY.config import BATTLE_CONFIG


@dataclass
class BattleChargeTracker:
    normal_attacks: int = 0

    @property
    def special_ready(self) -> bool:
        return self.normal_attacks >= BATTLE_CONFIG.special_charge_required

    def record_normal_attack(self) -> None:
        self.normal_attacks = min(
            BATTLE_CONFIG.special_charge_required,
            self.normal_attacks + 1,
        )

    def consume_special_attack(self) -> bool:
        if not self.special_ready:
            return False
        self.normal_attacks = 0
        return True

    def reset(self) -> None:
        self.normal_attacks = 0


def special_attack_damage(base_damage: int) -> int:
    return max(1, round(base_damage * BATTLE_CONFIG.special_damage_multiplier))


def xp_required_for_level(level: int) -> int:
    base_requirement = max(1, level) * BATTLE_CONFIG.base_xp_per_level
    return max(1, round(base_requirement * BATTLE_CONFIG.xp_requirement_multiplier))
