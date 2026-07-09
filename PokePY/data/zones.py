from dataclasses import dataclass

from PokePY.config import SCREEN_CONFIG

@dataclass(frozen=True)
class ZoneDefinition:
    name: str
    enemy_types: tuple[str, ...]
    difficulty: int
    encounter_rate: float
    item_rate: float
    grass_areas: tuple[tuple[int, int, int, int], ...]

ZONE_DEFINITIONS = (
    ZoneDefinition(
        name="Zona 1",
        enemy_types=("Fogo", "Água"),
        difficulty=1,
        encounter_rate=0.015,
        item_rate=0.2,
        grass_areas=(
            (50, 100, 150, 150),
            (450, 100, 150, 150),
            (200, 400, 150, 150),
            (650, 0, 150, 600),
        ),
    ),
    ZoneDefinition(
        name="Zona 2",
        enemy_types=("Planta", "Elétrico"),
        difficulty=2,
        encounter_rate=0.015,
        item_rate=0.2,
        grass_areas=(
            (50, 50, 700, 150),
            (100, 200, 150, 100),
            (300, 200, 150, 100),
            (500, 200, 150, 100),
            (100, 350, 150, 100),
            (300, 350, 150, 100),
            (500, 350, 150, 100),
            (150, 500, 100, 60),
            (400, 500, 200, 60),
        ),
    ),
    ZoneDefinition(
        name="Zona 3",
        enemy_types=("Pedra",),
        difficulty=3,
        encounter_rate=0.025,
        item_rate=0.2,
        grass_areas=(
            (0, 0, SCREEN_CONFIG.width, SCREEN_CONFIG.height // 2 - 50),
            (0, SCREEN_CONFIG.height // 2 + 50, SCREEN_CONFIG.width, SCREEN_CONFIG.height // 2 - 50),
        ),
    ),
)
