import math

import pygame

from PokePY.config import ITEM_CONFIG, PLAYER_CONFIG, SCREEN_CONFIG, UI_CONFIG
from PokePY.domain.models import Player
from PokePY.infrastructure.assets import AssetLoader
from PokePY.ui import colors
from PokePY.ui.fonts import FontBook
from PokePY.ui.widgets import draw_text

class PlayerSpriteAnimator:
    def __init__(self, assets: AssetLoader):
        self.assets = assets
        self.direction = "Frente"
        self.frame = 0
        self.timer_ms = 0
        self.last_valid_sprite = self.assets.load_player_sprite(self.direction, self.frame)

    def update(self, current_time_ms: int, moved: bool):
        if moved:
            if current_time_ms - self.timer_ms > PLAYER_CONFIG.animation_interval_ms:
                next_frame = self.frame + 1
                if next_frame < PLAYER_CONFIG.animation_first_frame or next_frame > PLAYER_CONFIG.animation_last_frame:
                    next_frame = PLAYER_CONFIG.animation_first_frame
                self.frame = next_frame
                self.timer_ms = current_time_ms
        else:
            self.frame = 0
        sprite = self.assets.load_player_sprite(self.direction, self.frame)
        if sprite is None:
            return self.last_valid_sprite
        self.last_valid_sprite = sprite
        return sprite

class ExplorationView:
    def __init__(self, fonts: FontBook, assets: AssetLoader):
        self.fonts = fonts
        self.assets = assets

    def draw_map(self, screen: pygame.Surface, zone_name: str):
        mask = self.assets.load_zone_mask(zone_name)
        background = self.assets.load_zone_background(zone_name)
        if mask:
            screen.blit(mask, (0, 0))
        if background:
            screen.blit(background, (0, 0))
        if not mask and not background:
            screen.fill(colors.DARK_GREEN)

    def draw_player(self, screen: pygame.Surface, player: Player, sprite):
        if sprite:
            sprite_x = player.x - sprite.get_width() // 2
            sprite_y = player.y - sprite.get_height()
            screen.blit(sprite, (sprite_x, sprite_y))
        else:
            pygame.draw.circle(screen, colors.BLUE, (player.x, player.y), 10)

    def draw_hud(self, screen: pygame.Surface, player: Player, zone_name: str, current_time_ms: int):
        hud_rect = pygame.Rect(20, 15, 260, 44)
        pygame.draw.rect(screen, colors.HUD_SHADOW, hud_rect.move(2, 2), border_radius=14)
        pygame.draw.rect(screen, colors.HUD_BACKGROUND, hud_rect, border_radius=14)
        pygame.draw.rect(screen, colors.HUD_BORDER, hud_rect, 2, border_radius=14)
        draw_text(screen, self.fonts, zone_name, hud_rect.x + 14, hud_rect.y + 10, color=colors.HUD_TEXT, font=self.fonts.small)
        if player.repel_active:
            remaining = max(0, player.repel_end_time_ms - current_time_ms)
            ratio = min(1.0, remaining / ITEM_CONFIG.repel_duration_ms)
            pygame.draw.rect(screen, (190, 210, 240), (hud_rect.x + 14, hud_rect.y + 28, 110, 6), border_radius=4)
            pygame.draw.rect(screen, (70, 140, 255), (hud_rect.x + 14, hud_rect.y + 28, int(110 * ratio), 6), border_radius=4)
            repel_text = f"Repelente ativo ({remaining // 1000}s)"
            repel_color = colors.REPEL_ACTIVE
        else:
            repel_text = "Repelente inativo"
            repel_color = colors.REPEL_INACTIVE
        surface = self.fonts.small.render(repel_text, True, repel_color)
        rect = surface.get_rect(topright=(hud_rect.right - 10, hud_rect.y + 10))
        screen.blit(surface, rect)

    def draw_backpack_button(self, screen: pygame.Surface) -> tuple[tuple[int, int], int]:
        center = (SCREEN_CONFIG.width - 80, 70)
        radius = UI_CONFIG.backpack_button_radius
        pygame.draw.circle(screen, (90, 140, 250), center, radius)
        pygame.draw.circle(screen, colors.WHITE, center, radius, 2)
        icon = self.assets.load_backpack_icon(int(radius * 1.3))
        if icon:
            screen.blit(icon, icon.get_rect(center=center))
        else:
            text = self.fonts.large.render("B", True, colors.BLACK)
            screen.blit(text, text.get_rect(center=center))
        return center, radius


    def draw_multiplayer_button(self, screen: pygame.Surface) -> pygame.Rect:
        rect = pygame.Rect(SCREEN_CONFIG.width - 185, 112, 130, 38)
        pygame.draw.rect(screen, (64, 86, 190), rect, border_radius=12)
        pygame.draw.rect(screen, colors.WHITE, rect, 2, border_radius=12)
        draw_text(screen, self.fonts, "Online [M]", rect.centerx, rect.centery, color=colors.WHITE, font=self.fonts.normal, center=True)
        return rect

    def click_hits_backpack(self, mouse_pos, button_center, radius: int) -> bool:
        return math.hypot(mouse_pos[0] - button_center[0], mouse_pos[1] - button_center[1]) <= radius

    def draw_item_message(self, screen: pygame.Surface, message: str | None, timer_ms: int, current_time_ms: int) -> str | None:
        if message and current_time_ms < timer_ms:
            draw_text(screen, self.fonts, message, 50, SCREEN_CONFIG.height - 50, color=colors.BLACK, font=self.fonts.large)
            return message
        return None
