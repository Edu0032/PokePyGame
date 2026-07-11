import pygame

from PokePY.config import SCREEN_CONFIG
from PokePY.services.leaderboard_contracts import LeaderboardEntry
from PokePY.services.time_formatter import format_seconds
from PokePY.ui import colors
from PokePY.ui.fonts import FontBook
from PokePY.ui.widgets import (
    draw_rounded_box,
    draw_styled_button,
    draw_text,
    is_button_clicked,
)


class LeaderboardView:
    def __init__(self, fonts: FontBook):
        self.fonts = fonts
        self.clock = pygame.time.Clock()

    def _draw_table(
        self,
        screen: pygame.Surface,
        entries: list[LeaderboardEntry],
        panel: pygame.Rect,
    ) -> None:
        header_y = panel.y + 125
        draw_text(
            screen,
            self.fonts,
            "#",
            panel.x + 50,
            header_y,
            color=colors.TEXT_COLOR_DARK,
            font=self.fonts.large,
            center_y=True,
        )
        draw_text(
            screen,
            self.fonts,
            "Treinador",
            panel.x + 105,
            header_y,
            color=colors.TEXT_COLOR_DARK,
            font=self.fonts.large,
            center_y=True,
        )
        draw_text(
            screen,
            self.fonts,
            "Tempo",
            panel.right - 80,
            header_y,
            color=colors.TEXT_COLOR_DARK,
            font=self.fonts.large,
            center=True,
        )
        pygame.draw.line(
            screen,
            colors.PANEL_BORDER,
            (panel.x + 35, header_y + 25),
            (panel.right - 35, header_y + 25),
            2,
        )
        if not entries:
            draw_text(
                screen,
                self.fonts,
                "Nenhum tempo salvo ainda.",
                panel.centerx,
                panel.centery,
                color=colors.TEXT_COLOR_DARK,
                font=self.fonts.large,
                center=True,
            )
            return
        for index, entry in enumerate(entries[:10], start=1):
            y = header_y + 35 + index * 32
            draw_text(
                screen,
                self.fonts,
                index,
                panel.x + 50,
                y,
                color=colors.BLACK,
                font=self.fonts.normal,
                center_y=True,
            )
            draw_text(
                screen,
                self.fonts,
                entry.player_name[:20],
                panel.x + 105,
                y,
                color=colors.BLACK,
                font=self.fonts.normal,
                center_y=True,
            )
            draw_text(
                screen,
                self.fonts,
                format_seconds(entry.elapsed_seconds),
                panel.right - 80,
                y,
                color=colors.BLACK,
                font=self.fonts.normal,
                center=True,
            )

    def draw(
        self,
        screen: pygame.Surface,
        entries: list[LeaderboardEntry],
        title: str,
        subtitle: str,
        footer: str,
        mouse_pos,
    ) -> tuple[pygame.Rect, pygame.Rect]:
        screen.fill(colors.BG_COLOR_MENU)
        panel = pygame.Rect(90, 60, 620, 520)
        draw_rounded_box(
            screen,
            panel,
            colors.MENU_BOX_COLOR,
            radius=18,
            shadow_color=colors.SHADOW_COLOR_DARK,
            shadow_offset=(6, 6),
        )
        pygame.draw.rect(screen, colors.PANEL_BORDER, panel, 2, border_radius=18)
        draw_text(
            screen,
            self.fonts,
            title,
            panel.centerx,
            panel.y + 42,
            color=colors.DARK_BLUE,
            font=self.fonts.xl,
            center=True,
        )
        draw_text(
            screen,
            self.fonts,
            subtitle,
            panel.centerx,
            panel.y + 82,
            color=colors.HUD_TEXT,
            font=self.fonts.normal,
            center=True,
        )
        self._draw_table(screen, entries, panel)
        draw_text(
            screen,
            self.fonts,
            footer,
            panel.centerx,
            panel.bottom - 112,
            color=colors.HUD_TEXT,
            font=self.fonts.normal,
            center=True,
        )
        play_again = pygame.Rect(panel.centerx - 230, panel.bottom - 70, 210, 48)
        exit_button = pygame.Rect(panel.centerx + 20, panel.bottom - 70, 210, 48)
        draw_styled_button(
            screen,
            self.fonts,
            "Jogar novamente",
            play_again,
            colors.BLACK,
            colors.CONFIRM_COLOR_OK,
            colors.SELECTED_COLOR_LIGHT,
            mouse_pos=mouse_pos,
            font=self.fonts.normal,
        )
        draw_styled_button(
            screen,
            self.fonts,
            "Sair",
            exit_button,
            colors.BLACK,
            colors.CONFIRM_COLOR_BAD,
            colors.BAG_RED,
            mouse_pos=mouse_pos,
            font=self.fonts.normal,
        )
        return play_again, exit_button

    def draw_browser(
        self,
        screen: pygame.Surface,
        entries: list[LeaderboardEntry],
        error_text: str | None,
        mouse_pos,
    ) -> pygame.Rect:
        screen.fill(colors.BG_COLOR_MENU)
        panel = pygame.Rect(90, 60, 620, 520)
        draw_rounded_box(
            screen,
            panel,
            colors.MENU_BOX_COLOR,
            radius=18,
            shadow_color=colors.SHADOW_COLOR_DARK,
            shadow_offset=(6, 6),
        )
        pygame.draw.rect(screen, colors.PANEL_BORDER, panel, 2, border_radius=18)
        draw_text(
            screen,
            self.fonts,
            "Ranking online",
            panel.centerx,
            panel.y + 42,
            color=colors.DARK_BLUE,
            font=self.fonts.xl,
            center=True,
        )
        subtitle = error_text or "Melhores tempos para zerar o jogo"
        draw_text(
            screen,
            self.fonts,
            subtitle,
            panel.centerx,
            panel.y + 82,
            color=colors.RED if error_text else colors.HUD_TEXT,
            font=self.fonts.small if error_text else self.fonts.normal,
            center=True,
        )
        self._draw_table(screen, entries, panel)
        back_button = pygame.Rect(panel.centerx - 125, panel.bottom - 68, 250, 46)
        draw_styled_button(
            screen,
            self.fonts,
            "Voltar [R/ESC]",
            back_button,
            colors.BLACK,
            colors.GRAY,
            colors.LIGHT_GRAY,
            mouse_pos=mouse_pos,
            font=self.fonts.normal,
        )
        return back_button

    def show(
        self,
        screen: pygame.Surface,
        entries: list[LeaderboardEntry],
        title: str,
        subtitle: str,
        footer: str,
    ) -> str:
        while True:
            mouse_pos = pygame.mouse.get_pos()
            play_again, exit_button = self.draw(
                screen,
                entries,
                title,
                subtitle,
                footer,
                mouse_pos,
            )
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                if event.type == pygame.KEYDOWN:
                    if event.key in {pygame.K_RETURN, pygame.K_r}:
                        return "restart"
                    if event.key in {pygame.K_ESCAPE, pygame.K_q}:
                        return "exit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = pygame.mouse.get_pos()
                    if is_button_clicked(click_pos, play_again):
                        return "restart"
                    if is_button_clicked(click_pos, exit_button):
                        return "exit"
            self.clock.tick(SCREEN_CONFIG.fps)
