import random

from PokePY.config import BATTLE_CONFIG
from PokePY.data.pokemon_catalog import BOSS_NAME
from PokePY.domain.game_state import BattleResult
from PokePY.domain.models import Player, Pokemon
from PokePY.services.combat_rules import special_attack_damage


class BattleEngine:
    def __init__(self, rng: random.Random | None = None):
        self.rng = rng or random.Random()

    def player_attack(
        self,
        attacker: Pokemon,
        defender: Pokemon,
        attack_index: int,
    ) -> tuple[str, int]:
        if attack_index == 0:
            damage = self.rng.randint(
                BATTLE_CONFIG.basic_damage_min,
                BATTLE_CONFIG.basic_damage_max,
            )
            attack_name = "Ataque Básico"
        else:
            base_damage = self.rng.randint(
                BATTLE_CONFIG.special_damage_min,
                BATTLE_CONFIG.special_damage_max,
            )
            damage = special_attack_damage(base_damage)
            attack_name = "Ataque Especial"
        defender.take_damage(damage)
        return attack_name, damage

    def enemy_attack(self, enemy: Pokemon, target: Pokemon) -> int:
        damage = self.rng.randint(
            BATTLE_CONFIG.enemy_damage_min,
            BATTLE_CONFIG.enemy_damage_max,
        )
        if enemy.name == BOSS_NAME:
            damage *= BATTLE_CONFIG.boss_damage_multiplier
        target.take_damage(damage)
        return damage

    def reward_victory(self, winner: Pokemon, defeated: Pokemon) -> None:
        winner.gain_xp(BATTLE_CONFIG.xp_multiplier * defeated.level)

    def heal_active_pokemon(self, player: Player, pokemon: Pokemon) -> bool:
        if player.items.get("Poção", 0) <= 0:
            return False
        pokemon.heal(BATTLE_CONFIG.potion_heal)
        player.items["Poção"] -= 1
        return True

    def try_flee(self, enemy: Pokemon) -> BattleResult | None:
        if enemy.name == BOSS_NAME:
            return BattleResult.FLEE_BLOCKED
        if self.rng.random() < BATTLE_CONFIG.flee_chance:
            return BattleResult.FLED
        return None
