from PokePY.data.assets import SPRITE_MAP
from PokePY.data.pokemon_catalog import PLAYER_POKEMON
from PokePY.domain.models import Pokemon


class PokemonFactory:
    def create(self, name: str, type_name: str, level: int = 1, hp: int = 100) -> Pokemon:
        return Pokemon(name=name, type=type_name, level=level, hp=hp)

    def starter_options(self) -> list[Pokemon]:
        return [self.create(data["name"], data["type"]) for data in PLAYER_POKEMON]

    def can_render(self, pokemon_name: str) -> bool:
        return pokemon_name in SPRITE_MAP
