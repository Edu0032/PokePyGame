import pygame

from PokePY.config import PLAYER_CONFIG, SCREEN_CONFIG, UI_CONFIG
from PokePY.domain.models import Pokemon
from PokePY.ui import colors
from PokePY.ui.fonts import FontBook
from PokePY.ui.widgets import draw_rounded_box, draw_text


class TeamSelectionView:
    def __init__(self, fonts: FontBook, pokemon_options: list[Pokemon]):
        self.fonts = fonts
        self.pokemon_options = pokemon_options

    def draw(
        self, screen: pygame.Surface, selected_pokemon: list[Pokemon]
    ) -> tuple[list[tuple[pygame.Rect, Pokemon]], pygame.Rect]:
        menu_height = (
            30
            + 60
            + 40
            + len(self.pokemon_options) * UI_CONFIG.team_button_height
            + (len(self.pokemon_options) - 1) * UI_CONFIG.team_button_padding
            + 30
            + UI_CONFIG.team_button_height
            + 30
        )
        menu_x = (SCREEN_CONFIG.width - UI_CONFIG.team_menu_width) // 2
        menu_y = (SCREEN_CONFIG.height - menu_height) // 2
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(colors.BG_COLOR_MENU)
        menu_rect = pygame.Rect(menu_x, menu_y, UI_CONFIG.team_menu_width, menu_height)
        draw_rounded_box(
            screen,
            menu_rect,
            colors.MENU_BOX_COLOR,
            radius=15,
            shadow_color=colors.SHADOW_COLOR_DARK,
            shadow_offset=(5, 5),
        )
        y_cursor = menu_y + 30
        draw_text(
            screen,
            self.fonts,
            "Selecione seu Time",
            menu_x + UI_CONFIG.team_menu_width // 2,
            y_cursor + 20,
            color=colors.TEXT_COLOR_DARK,
            font=self.fonts.xl,
            center=True,
        )
        y_cursor += 60
        draw_text(
            screen,
            self.fonts,
            f"Selecionado: {len(selected_pokemon)}/{PLAYER_CONFIG.team_size}",
            menu_x + UI_CONFIG.team_menu_width // 2,
            y_cursor,
            color=colors.TEXT_COLOR_DARK,
            font=self.fonts.large,
            center=True,
        )
        y_cursor += 40
        buttons = []
        button_width = UI_CONFIG.team_menu_width - 60
        selected_names = {pokemon.name for pokemon in selected_pokemon}
        for pokemon in self.pokemon_options:
            selected = pokemon.name in selected_names
            rect = pygame.Rect(menu_x + 30, y_cursor, button_width, UI_CONFIG.team_button_height)
            hovered = rect.collidepoint(mouse_pos)
            if selected:
                button_color = colors.SELECTED_COLOR_LIGHT
                shadow = colors.SHADOW_COLOR_LIGHT
            elif hovered:
                button_color = colors.BUTTON_HOVER_COLOR
                shadow = colors.SHADOW_COLOR_DARK
            else:
                button_color = colors.BUTTON_NORMAL_COLOR
                shadow = colors.SHADOW_COLOR_LIGHT
            draw_rounded_box(screen, rect, button_color, radius=10, shadow_color=shadow, shadow_offset=(2, 2))
            draw_text(
                screen,
                self.fonts,
                f"{pokemon.name} ({pokemon.type})",
                rect.centerx,
                rect.centery,
                color=colors.TEXT_COLOR_DARK,
                font=self.fonts.large,
                center=True,
            )
            buttons.append((rect, pokemon))
            y_cursor += UI_CONFIG.team_button_height + UI_CONFIG.team_button_padding
        y_cursor += 30
        confirm_rect = pygame.Rect(menu_x + 30, y_cursor, button_width, UI_CONFIG.team_button_height)
        can_confirm = len(selected_pokemon) == PLAYER_CONFIG.team_size
        confirm_color: tuple[int, int, int] = colors.CONFIRM_COLOR_OK if can_confirm else colors.CONFIRM_COLOR_BAD
        if confirm_rect.collidepoint(mouse_pos):
            confirm_color = tuple(min(value + 20, 255) for value in confirm_color)  # type: ignore[assignment]
        draw_rounded_box(
            screen, confirm_rect, confirm_color, radius=10, shadow_color=colors.SHADOW_COLOR_DARK, shadow_offset=(2, 2)
        )
        draw_text(
            screen,
            self.fonts,
            "Confirmar Time",
            confirm_rect.centerx,
            confirm_rect.centery,
            color=colors.TEXT_COLOR_LIGHT,
            font=self.fonts.large,
            center=True,
        )
        return buttons, confirm_rect
