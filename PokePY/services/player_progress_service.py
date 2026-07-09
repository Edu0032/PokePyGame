from dataclasses import asdict, dataclass

from PokePY.domain.models import Player, Pokemon
from PokePY.services.player_progress_contracts import PlayerProgressRepository

@dataclass(frozen=True)
class PokemonProgress:
    name: str
    type: str
    level: int
    hp: int
    max_hp: int
    xp: int
    attacks: list[str]
    evolution_stage: int

@dataclass(frozen=True)
class PlayerProgress:
    player_id: str
    player_name: str
    zone_index: int
    x: int
    y: int
    items: dict[str, int]
    team: list[PokemonProgress]

class PlayerProgressService:
    def __init__(self, repository: PlayerProgressRepository | None):
        self.repository = repository

    def save(self, player_id: str, player: Player, player_name: str | None = None) -> None:
        progress = self.to_progress(player_id, player_name or player_id, player)
        if hasattr(self.repository, "save_progress"):
            self.repository.save_progress(progress)
            return
        self.repository.save(player_id, player)

    def load(self, player_id: str) -> Player | None:
        if hasattr(self.repository, "load_progress"):
            progress = self.repository.load_progress(player_id)
            return self.from_progress(progress) if progress else None
        return self.repository.load(player_id)

    def to_progress(self, player_id: str, player_name: str, player: Player) -> PlayerProgress:
        return PlayerProgress(
            player_id=player_id,
            player_name=player_name,
            zone_index=player.zone_index,
            x=player.x,
            y=player.y,
            items=player.items.copy(),
            team=[self._pokemon_to_progress(pokemon) for pokemon in player.team],
        )

    def from_progress(self, progress: PlayerProgress) -> Player:
        return Player(
            team=[self._progress_to_pokemon(pokemon) for pokemon in progress.team],
            items=progress.items.copy(),
            x=progress.x,
            y=progress.y,
            zone_index=progress.zone_index,
        )

    def to_dict(self, progress: PlayerProgress) -> dict:
        return asdict(progress)

    def from_dict(self, payload: dict) -> PlayerProgress:
        return PlayerProgress(
            player_id=str(payload["player_id"]),
            player_name=str(payload["player_name"]),
            zone_index=int(payload["zone_index"]),
            x=int(payload["x"]),
            y=int(payload["y"]),
            items={str(key): int(value) for key, value in dict(payload["items"]).items()},
            team=[self._progress_from_dict(item) for item in list(payload["team"])],
        )

    def _pokemon_to_progress(self, pokemon: Pokemon) -> PokemonProgress:
        return PokemonProgress(
            name=pokemon.name,
            type=pokemon.type,
            level=pokemon.level,
            hp=pokemon.hp,
            max_hp=pokemon.max_hp,
            xp=pokemon.xp,
            attacks=pokemon.attacks.copy(),
            evolution_stage=pokemon.evolution_stage,
        )

    def _progress_to_pokemon(self, progress: PokemonProgress) -> Pokemon:
        return Pokemon(
            name=progress.name,
            type=progress.type,
            level=progress.level,
            hp=progress.hp,
            max_hp=progress.max_hp,
            xp=progress.xp,
            attacks=progress.attacks.copy(),
            evolution_stage=progress.evolution_stage,
        )

    def _progress_from_dict(self, payload: dict) -> PokemonProgress:
        return PokemonProgress(
            name=str(payload["name"]),
            type=str(payload["type"]),
            level=int(payload["level"]),
            hp=int(payload["hp"]),
            max_hp=int(payload["max_hp"]),
            xp=int(payload["xp"]),
            attacks=[str(attack) for attack in list(payload["attacks"])],
            evolution_stage=int(payload["evolution_stage"]),
        )
