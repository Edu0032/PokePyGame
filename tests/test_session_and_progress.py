from pathlib import Path

from PokePY.domain.models import Player, Pokemon
from PokePY.domain.session import GameSession
from PokePY.infrastructure.json_player_progress_repository import JsonPlayerProgressRepository
from PokePY.services.multiplayer_contracts import PlayerSnapshot, PokemonSnapshot
from PokePY.services.player_progress_service import PlayerProgressService


class MemoryRepository:
    def __init__(self):
        self.storage = {}

    def save(self, player_id, player):
        self.storage[player_id] = player

    def load(self, player_id):
        return self.storage.get(player_id)


def test_session_elapsed_time_uses_provider():
    values = iter([10.0, 75.0])
    session = GameSession(time_provider=lambda: next(values))
    session.start()
    session.finish()
    assert session.elapsed_seconds == 65


def test_player_progress_roundtrip():
    service = PlayerProgressService(MemoryRepository())
    player = Player(
        team=[Pokemon("Pikachu", "Elétrico", level=3, hp=90, max_hp=120, xp=25)],
        items={"Poção": 2},
        x=100,
        y=200,
        zone_index=1,
    )
    progress = service.to_progress("player-1", "Ana", player)
    restored = service.from_progress(progress)
    assert restored.team[0].name == "Pikachu"
    assert restored.team[0].level == 3
    assert restored.items["Poção"] == 2
    assert restored.zone_index == 1


def test_json_player_progress_repository_roundtrip(tmp_path: Path):
    repository = JsonPlayerProgressRepository(tmp_path)
    player = Player(
        team=[Pokemon("Bulbasaur", "Grama", level=4, hp=70, max_hp=120)], items={"Poção": 1}, x=15, y=25, zone_index=2
    )
    repository.save("Player_1", player)
    restored = repository.load("Player_1")
    assert restored is not None
    assert restored.team[0].name == "Bulbasaur"
    assert restored.team[0].level == 4
    assert restored.zone_index == 2


def test_multiplayer_snapshot_from_pokemon():
    pokemon = Pokemon("Squirtle", "Água", level=2, hp=80, max_hp=100)
    snapshot = PokemonSnapshot.from_pokemon(pokemon)
    player_snapshot = PlayerSnapshot("p1", "Jogador 1", (snapshot,), items={"Poção": 1})
    assert player_snapshot.team[0].name == "Squirtle"
    assert player_snapshot.items["Poção"] == 1


def test_same_display_name_sessions_have_unique_multiplayer_ids():
    first = GameSession()
    second = GameSession()
    first.identify_player("Mesmo Nome")
    second.identify_player("Mesmo Nome")
    assert first.player_id == second.player_id
    assert first.multiplayer_player_id != second.multiplayer_player_id
