import pygame

from PokePY.ui import colors
from PokePY.ui.fonts import FontBook
from PokePY.ui.widgets import draw_rounded_box, draw_styled_button, draw_text, is_button_clicked


class PlayerNameView:
    def __init__(self, fonts: FontBook, max_length: int = 16):
        self.fonts = fonts
        self.max_length = max_length

    def draw(self, screen: pygame.Surface, player_name: str, mouse_pos) -> pygame.Rect:
        screen.fill(colors.BG_COLOR_MENU)
        panel = pygame.Rect(135, 130, 530, 360)
        draw_rounded_box(
            screen, panel, colors.MENU_BOX_COLOR, radius=18, shadow_color=colors.SHADOW_COLOR_DARK, shadow_offset=(6, 6)
        )
        pygame.draw.rect(screen, colors.PANEL_BORDER, panel, 2, border_radius=18)
        draw_text(
            screen,
            self.fonts,
            "PokePy",
            panel.centerx,
            panel.y + 52,
            color=colors.DARK_BLUE,
            font=self.fonts.xl,
            center=True,
        )
        draw_text(
            screen,
            self.fonts,
            "Digite seu nome de treinador",
            panel.centerx,
            panel.y + 105,
            color=colors.TEXT_COLOR_DARK,
            font=self.fonts.large,
            center=True,
        )
        input_rect = pygame.Rect(panel.x + 65, panel.y + 150, panel.width - 130, 58)
        draw_rounded_box(
            screen, input_rect, colors.WHITE, radius=10, shadow_color=colors.SHADOW_COLOR_LIGHT, shadow_offset=(2, 2)
        )
        pygame.draw.rect(screen, colors.BATTLE_MENU_BORDER, input_rect, 2, border_radius=10)
        name_text = player_name if player_name else "Treinador"
        draw_text(
            screen,
            self.fonts,
            name_text,
            input_rect.x + 18,
            input_rect.centery,
            color=colors.BLACK,
            font=self.fonts.large,
            center_y=True,
        )
        draw_text(
            screen,
            self.fonts,
            "ENTER ou botão para iniciar",
            panel.centerx,
            input_rect.bottom + 38,
            color=colors.HUD_TEXT,
            font=self.fonts.normal,
            center=True,
        )
        button = pygame.Rect(panel.centerx - 135, panel.bottom - 85, 270, 52)
        draw_styled_button(
            screen,
            self.fonts,
            "Começar Jornada",
            button,
            colors.BLACK,
            colors.CONFIRM_COLOR_OK,
            colors.SELECTED_COLOR_LIGHT,
            mouse_pos=mouse_pos,
            font=self.fonts.large,
        )
        return button

    def normalize_input(self, current_text: str, event: pygame.event.Event) -> str:
        if event.key == pygame.K_BACKSPACE:
            return current_text[:-1]
        if event.key in {pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_ESCAPE}:
            return current_text
        char = event.unicode
        if not char or len(current_text) >= self.max_length:
            return current_text
        if char.isalnum() or char in {" ", "_", "-"}:
            return current_text + char
        return current_text

    def should_start(self, event: pygame.event.Event, start_button: pygame.Rect | None = None) -> bool:
        if event.type == pygame.KEYDOWN and event.key in {pygame.K_RETURN, pygame.K_KP_ENTER}:
            return True
        if event.type == pygame.MOUSEBUTTONDOWN and start_button is not None:
            return is_button_clicked(pygame.mouse.get_pos(), start_button)
        return False
