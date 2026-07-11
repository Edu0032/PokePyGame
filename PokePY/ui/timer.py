import pygame

from PokePY.config import SCREEN_CONFIG
from PokePY.services.time_formatter import format_seconds
from PokePY.ui import colors
from PokePY.ui.fonts import FontBook
from PokePY.ui.widgets import draw_text


class RunTimerView:
    def __init__(self, fonts: FontBook):
        self.fonts = fonts

    def draw(self, screen: pygame.Surface, elapsed_seconds: int):
        timer_text = f"Tempo: {format_seconds(elapsed_seconds)}"
        draw_text(
            screen,
            self.fonts,
            timer_text,
            SCREEN_CONFIG.width - 18,
            22,
            color=colors.HUD_TEXT,
            font=self.fonts.normal,
            align_right=True,
        )
