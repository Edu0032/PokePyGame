from dataclasses import dataclass, field

from PokePY.config import ITEM_CONFIG, PLAYER_CONFIG
from PokePY.data.pokemon_catalog import DEFAULT_ATTACKS

@dataclass
class Pokemon:
    name: str
    type: str
    level: int = 1
    hp: int = 100
    max_hp: int | None = None
    xp: int = 0
    attacks: list[str] = field(default_factory=lambda: DEFAULT_ATTACKS.copy())
    evolution_stage: int = 0

    def __post_init__(self):
        if self.max_hp is None:
            self.max_hp = self.hp

    def clone(self) -> "Pokemon":
        return Pokemon(
            name=self.name,
            type=self.type,
            level=self.level,
            hp=self.hp,
            max_hp=self.max_hp,
            xp=self.xp,
            attacks=self.attacks.copy(),
            evolution_stage=self.evolution_stage,
        )

    def gain_xp(self, amount: int):
        self.xp += amount
        while self.xp >= self.level * 100:
            self.xp -= self.level * 100
            self.level += 1
            self.max_hp += 20
            self.hp = min(self.hp + 20, self.max_hp)
            if self.level % 3 == 0 and self.evolution_stage < 1:
                self.evolve()

    def evolve(self):
        self.evolution_stage += 1
        self.max_hp += 50
        self.hp = min(self.hp + 50, self.max_hp)
        if "Ataque Especial" not in self.attacks:
            self.attacks.insert(1, "Ataque Especial")

    def take_damage(self, damage: int):
        self.hp = max(0, self.hp - max(0, damage))

    def heal(self, amount: int):
        self.hp = min(self.max_hp, self.hp + max(0, amount))

    def is_alive(self) -> bool:
        return self.hp > 0

@dataclass
class Player:
    team: list[Pokemon] = field(default_factory=list)
    items: dict[str, int] = field(default_factory=lambda: ITEM_CONFIG.initial_items.copy())
    repel_active: bool = False
    repel_end_time_ms: int = 0
    repel_pending: bool = False
    x: int = PLAYER_CONFIG.start_x
    y: int = PLAYER_CONFIG.start_y
    zone_index: int = 0

    def add_pokemon(self, pokemon: Pokemon) -> bool:
        if len(self.team) >= PLAYER_CONFIG.team_size:
            return False
        self.team.append(pokemon)
        return True

    def first_alive_pokemon(self) -> Pokemon | None:
        return next((pokemon for pokemon in self.team if pokemon.is_alive()), None)

    def has_alive_pokemon(self) -> bool:
        return self.first_alive_pokemon() is not None

    def use_item(self, item_name: str) -> bool:
        if self.items.get(item_name, 0) <= 0:
            return False
        self.items[item_name] -= 1
        if item_name == "Repelente":
            self.repel_pending = True
        return True

    def add_item(self, item_name: str) -> bool:
        cap = ITEM_CONFIG.item_caps.get(item_name, 999)
        if self.items.get(item_name, 0) >= cap:
            return False
        self.items[item_name] = self.items.get(item_name, 0) + 1
        return True

    def activate_pending_repel(self, current_time_ms: int):
        if not self.repel_pending:
            return
        self.repel_active = True
        self.repel_end_time_ms = current_time_ms + ITEM_CONFIG.repel_duration_ms
        self.repel_pending = False

    def update_repel(self, current_time_ms: int):
        if self.repel_active and current_time_ms > self.repel_end_time_ms:
            self.repel_active = False
