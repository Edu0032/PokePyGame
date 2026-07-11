import random

from PokePY.data.assets import SPRITE_MAP
from PokePY.data.pokemon_catalog import ENEMY_NAMES_BY_TYPE
from PokePY.data.zones import ZoneDefinition
from PokePY.domain.factories import PokemonFactory
from PokePY.domain.models import Pokemon


class EncounterService:
    def __init__(self, pokemon_factory: PokemonFactory, rng: random.Random | None = None):
        self.pokemon_factory = pokemon_factory
        self.rng = rng or random.Random()

    def random_encounter(self, zone: ZoneDefinition) -> Pokemon | None:
        if self.rng.random() >= zone.encounter_rate:
            return None
        possible_names = self._enemy_names_for_zone(zone)
        if not possible_names:
            return None
        enemy_name, enemy_type = self.rng.choice(possible_names)
        return self.pokemon_factory.create(enemy_name, enemy_type, level=zone.difficulty)

    def random_item(
        self, zone: ZoneDefinition, player_x: int, screen_width: int, boss_distance_from_right: int
    ) -> str | None:
        if self.rng.random() >= zone.item_rate:
            return None
        if zone.name == "Zona 3" and player_x > screen_width - boss_distance_from_right:
            return None
        return self.rng.choice(["Poção", "Repelente"])

    def _enemy_names_for_zone(self, zone: ZoneDefinition) -> list[tuple[str, str]]:
        result: list[tuple[str, str]] = []
        for enemy_type in zone.enemy_types:
            result.extend((name, enemy_type) for name in ENEMY_NAMES_BY_TYPE.get(enemy_type, []) if name in SPRITE_MAP)
        return result
