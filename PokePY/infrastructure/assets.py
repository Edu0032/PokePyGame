from pathlib import Path

import pygame

from PokePY.config import ASSET_DIR, PLAYER_CONFIG, SCREEN_CONFIG
from PokePY.data.assets import AVATAR_BASE, BACKPACK_ICON, BATTLE_BACKGROUNDS, SPRITE_MAP, ZONE_MAPS, ZONE_MASKS


class AssetLoader:
    def __init__(self, base_dir: Path = ASSET_DIR):
        self.base_dir = base_dir
        self.sprites: dict[tuple[str, str, int], pygame.Surface] = {}
        self.images: dict[tuple[str, bool], pygame.Surface] = {}
        self.scaled_images: dict[tuple[str, tuple[int, int], bool], pygame.Surface] = {}

    def load_sprite(self, pokemon_name: str, direction: str = "front", scale: int = 2) -> pygame.Surface | None:
        if pokemon_name == "Player Avatar":
            direction = "front"
            scale = 1
        key = (pokemon_name, direction, scale)
        if key in self.sprites:
            return self.sprites[key]
        path = SPRITE_MAP.get(pokemon_name, {}).get(direction)
        if not path:
            return None
        image = self.load_image(path, alpha=True)
        if image is None:
            return None
        width, height = image.get_size()
        image = pygame.transform.scale(image, (width * scale, height * scale))
        self.sprites[key] = image
        return image

    def load_player_sprite(self, direction: str, frame: int) -> pygame.Surface | None:
        filename = f"SpriteParado{direction}.png" if frame == 0 else f"New Piskel-{frame}.png"
        path = str(Path(AVATAR_BASE) / direction / filename)
        image = self.load_image(path, alpha=True)
        if image is None:
            return None
        return pygame.transform.scale(image, (PLAYER_CONFIG.sprite_size, PLAYER_CONFIG.sprite_size))

    def load_zone_background(self, zone_name: str) -> pygame.Surface | None:
        return self.load_scaled_image(ZONE_MAPS[zone_name], (SCREEN_CONFIG.width, SCREEN_CONFIG.height), alpha=False)

    def load_zone_mask(self, zone_name: str) -> pygame.Surface | None:
        return self.load_scaled_image(ZONE_MASKS[zone_name], (SCREEN_CONFIG.width, SCREEN_CONFIG.height), alpha=True)

    def load_battle_background(self, zone_name: str) -> pygame.Surface | None:
        path = BATTLE_BACKGROUNDS.get(zone_name)
        if not path:
            return None
        return self.load_scaled_image(path, (SCREEN_CONFIG.width, SCREEN_CONFIG.height), alpha=False)

    def load_backpack_icon(self, size: int) -> pygame.Surface | None:
        image = self.load_image(BACKPACK_ICON, alpha=True)
        if image is None:
            return None
        return pygame.transform.smoothscale(image, (size, size))

    def load_image(self, relative_path: str, alpha: bool) -> pygame.Surface | None:
        key = (relative_path, alpha)
        if key in self.images:
            return self.images[key]
        path = self.base_dir / relative_path
        if not path.exists():
            return None
        image = pygame.image.load(str(path))
        image = image.convert_alpha() if alpha else image.convert()
        self.images[key] = image
        return image

    def load_scaled_image(self, relative_path: str, size: tuple[int, int], alpha: bool) -> pygame.Surface | None:
        key = (relative_path, size, alpha)
        if key in self.scaled_images:
            return self.scaled_images[key]
        image = self.load_image(relative_path, alpha)
        if image is None:
            return None
        scaled = pygame.transform.scale(image, size)
        self.scaled_images[key] = scaled
        return scaled
