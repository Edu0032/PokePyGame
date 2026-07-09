import pygame

from PokePY.config import SCREEN_CONFIG, UI_CONFIG
from PokePY.ui import colors
from PokePY.ui.fonts import FontBook
from PokePY.ui.widgets import draw_rounded_box, draw_text

class GameOverView:
    def __init__(self, fonts: FontBook):
        self.fonts = fonts

    def draw(self, screen: pygame.Surface):
        overlay = pygame.Surface((SCREEN_CONFIG.width, SCREEN_CONFIG.height), pygame.SRCALPHA)
        overlay.fill(colors.OVERLAY_GAME_OVER)
        screen.blit(overlay, (0, 0))
        rect = pygame.Rect((SCREEN_CONFIG.width - UI_CONFIG.modal_width) // 2, (SCREEN_CONFIG.height - UI_CONFIG.modal_height) // 2, UI_CONFIG.modal_width, UI_CONFIG.modal_height)
        draw_rounded_box(screen, rect, colors.CONFIRM_COLOR_BAD, radius=15, shadow_color=colors.SHADOW_COLOR_DARK, shadow_offset=(5, 5))
        pygame.draw.rect(screen, colors.RED, rect, 3, border_radius=15)
        draw_text(screen, self.fonts, "GAME OVER", rect.centerx, rect.centery - 20, color=colors.TEXT_COLOR_LIGHT, font=self.fonts.xl, center=True)
        draw_text(screen, self.fonts, "Seu time desmaiou!", rect.centerx, rect.centery + 25, color=colors.TEXT_COLOR_LIGHT, font=self.fonts.normal, center=True)
