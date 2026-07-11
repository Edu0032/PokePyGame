from __future__ import annotations

import hashlib

import pygame

from PokePY.config import BATTLE_CONFIG, SCREEN_CONFIG
from PokePY.infrastructure.assets import AssetLoader
from PokePY.services.multiplayer_contracts import (
    MatchSnapshot,
    MatchStatus,
    PlayerSnapshot,
)
from PokePY.ui import colors
from PokePY.ui.battle import BattleView
from PokePY.ui.fonts import FontBook
from PokePY.ui.widgets import draw_rounded_box, draw_styled_button, draw_text


class MultiplayerLobbyView:
    def __init__(self, fonts: FontBook):
        self.fonts = fonts

    def draw(
        self,
        screen: pygame.Surface,
        status_text: str,
        error_text: str | None,
        mouse_pos,
    ):
        screen.fill((16, 24, 40))
        panel = pygame.Rect(100, 170, 600, 400)
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
            "Modo Multiplayer",
            panel.centerx,
            panel.y + 48,
            color=colors.DARK_BLUE,
            font=self.fonts.xl,
            center=True,
        )
        draw_text(
            screen,
            self.fonts,
            status_text,
            panel.centerx,
            panel.y + 130,
            color=colors.BLACK,
            font=self.fonts.large,
            center=True,
        )
        draw_text(
            screen,
            self.fonts,
            "A API cria uma fila e inicia a batalha quando outro jogador entrar.",
            panel.centerx,
            panel.y + 180,
            color=colors.BLACK,
            font=self.fonts.normal,
            center=True,
        )
        if error_text:
            draw_text(
                screen,
                self.fonts,
                error_text[:76],
                panel.centerx,
                panel.y + 230,
                color=colors.RED,
                font=self.fonts.small,
                center=True,
            )
        enter_rect = pygame.Rect(panel.centerx - 170, panel.bottom - 105, 340, 48)
        back_rect = pygame.Rect(panel.centerx - 170, panel.bottom - 50, 340, 40)
        draw_styled_button(
            screen,
            self.fonts,
            "Entrar na fila",
            enter_rect,
            mouse_pos=mouse_pos,
        )
        draw_styled_button(
            screen,
            self.fonts,
            "Voltar",
            back_rect,
            bg_color=colors.GRAY,
            hover_color=colors.GRAY,
            mouse_pos=mouse_pos,
        )
        return enter_rect, back_rect


class MultiplayerBattleView:
    def __init__(self, fonts: FontBook, assets: AssetLoader):
        self.fonts = fonts
        self.battle_view = BattleView(fonts, assets)

    def draw(
        self,
        screen: pygame.Surface,
        match: MatchSnapshot,
        player_id: str,
        switch_mode: bool,
        mouse_pos,
    ) -> dict:
        player = next(
            (item for item in match.players if item.player_id == player_id),
            None,
        )
        opponent = next(
            (item for item in match.players if item.player_id != player_id),
            None,
        )
        controls: dict = {}
        if player is None or opponent is None:
            screen.fill((16, 24, 40))
            draw_text(
                screen,
                self.fonts,
                "Partida inválida.",
                SCREEN_CONFIG.width // 2,
                SCREEN_CONFIG.height // 2,
                color=colors.WHITE,
                font=self.fonts.xl,
                center=True,
            )
            return controls
        player_pokemon = self._active_pokemon(player)
        opponent_pokemon = self._active_pokemon(opponent)
        if player_pokemon is None or opponent_pokemon is None:
            return controls

        self.battle_view.draw_battle_screen(
            screen,
            player_pokemon,
            opponent_pokemon,
            self._battle_zone(match.match_id),
        )
        self._draw_header(screen, match, player)
        draw_text(
            screen,
            self.fonts,
            f"Você: {player.player_name}",
            50,
            405,
            color=colors.WHITE,
            font=self.fonts.small,
        )
        draw_text(
            screen,
            self.fonts,
            f"Oponente: {opponent.player_name}",
            SCREEN_CONFIG.width - 250,
            145,
            color=colors.WHITE,
            font=self.fonts.small,
        )
        latest_event = match.events[-1] if match.events else "A batalha online começou."

        if match.status == MatchStatus.FINISHED:
            result = "Você venceu!" if match.winner_player_id == player_id else "Você perdeu."
            self.battle_view.draw_message_box(
                screen,
                f"{result} {latest_event}",
            )
            controls["leave"] = self.battle_view.draw_action_buttons(
                screen,
                ["Voltar ao mapa"],
                mouse_pos,
                keys=["ENTER"],
            )[0][0]
            return controls
        if match.active_player_id != player_id:
            self.battle_view.draw_message_box(
                screen,
                f"Aguardando o oponente... {latest_event}",
            )
            leave_rect = pygame.Rect(
                SCREEN_CONFIG.width - 160,
                SCREEN_CONFIG.height - 78,
                125,
                42,
            )
            draw_styled_button(
                screen,
                self.fonts,
                "Sair",
                leave_rect,
                bg_color=colors.GRAY,
                hover_color=colors.GRAY,
                mouse_pos=mouse_pos,
                font=self.fonts.normal,
            )
            controls["leave"] = leave_rect
            return controls
        if switch_mode:
            self.battle_view.draw_message_box(
                screen,
                "Escolha o Pokémon que entrará na batalha.",
            )
            controls["team"] = self._draw_team_choices(screen, player, mouse_pos)
            controls["back"] = pygame.Rect(560, 560, 160, 42)
            draw_styled_button(
                screen,
                self.fonts,
                "Cancelar",
                controls["back"],
                bg_color=colors.GRAY,
                hover_color=colors.GRAY,
                mouse_pos=mouse_pos,
                font=self.fonts.normal,
            )
            return controls

        special_ready = player.normal_attack_count >= BATTLE_CONFIG.special_charge_required
        primary_key = "special" if special_ready else "basic"
        primary_label = "Ataque Especial" if special_ready else "Ataque Básico"
        charge_text = (
            "Especial carregado."
            if special_ready
            else (f"Carga especial {player.normal_attack_count}/{BATTLE_CONFIG.special_charge_required}.")
        )
        self.battle_view.draw_message_box(
            screen,
            f"Sua vez. {charge_text} {latest_event}",
        )
        actions = [
            (primary_key, primary_label),
            ("heal", "Poção"),
            ("switch", "Trocar"),
            ("leave", "Sair"),
        ]
        buttons = self.battle_view.draw_action_buttons(
            screen,
            [label for _, label in actions],
            mouse_pos,
            keys=["X" if special_ready else "Z", "C", "V", "ESC"],
        )
        for (key, _), (rect, _) in zip(actions, buttons, strict=True):
            controls[key] = rect
        return controls

    def _draw_header(
        self,
        screen: pygame.Surface,
        match: MatchSnapshot,
        player: PlayerSnapshot,
    ) -> None:
        turn = "sua vez" if match.active_player_id == player.player_id else "vez do oponente"
        header = pygame.Rect(245, 12, 310, 44)
        draw_rounded_box(
            screen,
            header,
            colors.BATTLE_MENU_BG,
            radius=12,
            shadow_color=colors.SHADOW_COLOR_DARK,
            shadow_offset=(3, 3),
        )
        draw_text(
            screen,
            self.fonts,
            f"Online • turno {match.turn_number} • {turn}",
            header.centerx,
            header.centery,
            color=colors.DARK_BLUE,
            font=self.fonts.normal,
            center=True,
        )

    def _draw_team_choices(self, screen, player, mouse_pos):
        panel = pygame.Rect(70, 455, 660, 145)
        draw_rounded_box(
            screen,
            panel,
            colors.BATTLE_MENU_BG,
            radius=12,
            shadow_color=colors.SHADOW_COLOR_DARK,
            shadow_offset=(3, 3),
        )
        pygame.draw.rect(
            screen,
            colors.BATTLE_MENU_BORDER,
            panel,
            2,
            border_radius=12,
        )
        buttons = []
        for index, pokemon in enumerate(player.team):
            rect = pygame.Rect(panel.x + 20 + index * 210, panel.y + 48, 190, 45)
            disabled = pokemon.hp <= 0 or index == player.active_pokemon_index
            draw_styled_button(
                screen,
                self.fonts,
                f"{pokemon.name} {pokemon.hp}/{pokemon.max_hp}",
                rect,
                bg_color=(colors.LIGHT_GRAY if disabled else colors.BATTLE_BUTTON_NORMAL),
                hover_color=(colors.LIGHT_GRAY if disabled else colors.BATTLE_BUTTON_HOVER),
                mouse_pos=mouse_pos,
                font=self.fonts.small,
            )
            if not disabled:
                buttons.append((rect, index))
        return buttons

    def _battle_zone(self, match_id: str) -> str:
        digest = hashlib.sha256(match_id.encode("utf-8")).digest()
        return ("Zona 1", "Zona 2", "Zona 3")[digest[0] % 3]

    def _active_pokemon(self, player: PlayerSnapshot):
        if not player.team:
            return None
        return player.team[max(0, min(player.active_pokemon_index, len(player.team) - 1))]
