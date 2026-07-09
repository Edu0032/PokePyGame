import pygame

from PokePY.config import SCREEN_CONFIG
from PokePY.services.multiplayer_contracts import MatchSnapshot, PlayerSnapshot
from PokePY.ui import colors
from PokePY.ui.fonts import FontBook
from PokePY.ui.widgets import draw_rounded_box, draw_styled_button, draw_text

class MultiplayerLobbyView:
    def __init__(self, fonts: FontBook):
        self.fonts = fonts

    def draw(self, screen: pygame.Surface, status_text: str, error_text: str | None, mouse_pos) -> tuple[pygame.Rect, pygame.Rect]:
        screen.fill((16, 24, 40))
        panel = pygame.Rect(120, 120, SCREEN_CONFIG.width - 240, 360)
        draw_rounded_box(screen, panel, colors.BATTLE_MENU_BG, radius=18, shadow_color=colors.SHADOW_COLOR_DARK, shadow_offset=(5, 5))
        pygame.draw.rect(screen, colors.BATTLE_MENU_BORDER, panel, 2, border_radius=18)
        draw_text(screen, self.fonts, "Modo Multiplayer", panel.centerx, panel.y + 45, color=colors.DARK_BLUE, font=self.fonts.xl, center=True)
        draw_text(screen, self.fonts, status_text, panel.centerx, panel.y + 115, color=colors.BLACK, font=self.fonts.large, center=True)
        draw_text(screen, self.fonts, "A API cria uma fila e inicia a batalha quando outro jogador entrar.", panel.centerx, panel.y + 155, color=colors.BLACK, font=self.fonts.normal, center=True)
        if error_text:
            draw_text(screen, self.fonts, error_text, panel.centerx, panel.y + 205, color=colors.RED, font=self.fonts.normal, center=True)
        enter_rect = pygame.Rect(panel.centerx - 170, panel.bottom - 105, 340, 48)
        back_rect = pygame.Rect(panel.centerx - 170, panel.bottom - 50, 340, 40)
        draw_styled_button(screen, self.fonts, "Entrar na fila", enter_rect, mouse_pos=mouse_pos)
        draw_styled_button(screen, self.fonts, "Voltar", back_rect, bg_color=colors.GRAY, hover_color=colors.GRAY, mouse_pos=mouse_pos)
        return enter_rect, back_rect

class MultiplayerBattleView:
    def __init__(self, fonts: FontBook):
        self.fonts = fonts

    def draw(self, screen: pygame.Surface, match: MatchSnapshot, player_id: str, switch_mode: bool, mouse_pos) -> dict[str, pygame.Rect | list[tuple[pygame.Rect, int]]]:
        screen.fill((20, 72, 88))
        player = self._find_player(match, player_id)
        opponent = self._find_opponent(match, player_id)
        controls = {}
        if player is None or opponent is None:
            draw_text(screen, self.fonts, "Partida inválida.", SCREEN_CONFIG.width // 2, SCREEN_CONFIG.height // 2, color=colors.WHITE, font=self.fonts.xl, center=True)
            controls["leave"] = pygame.Rect(280, 520, 240, 45)
            draw_styled_button(screen, self.fonts, "Voltar", controls["leave"], mouse_pos=mouse_pos)
            return controls
        self._draw_header(screen, match, player_id)
        self._draw_pokemon_card(screen, opponent, pygame.Rect(60, 110, 300, 150), "Oponente")
        self._draw_pokemon_card(screen, player, pygame.Rect(440, 305, 300, 150), "Você")
        self._draw_events(screen, match)
        if match.status == "finished":
            message = "Você venceu!" if match.winner_player_id == player_id else "Você perdeu."
            draw_text(screen, self.fonts, message, SCREEN_CONFIG.width // 2, 500, color=colors.WHITE, font=self.fonts.xl, center=True)
            controls["leave"] = pygame.Rect(275, 555, 250, 45)
            draw_styled_button(screen, self.fonts, "Voltar ao mapa", controls["leave"], mouse_pos=mouse_pos)
            return controls
        if match.active_player_id != player_id:
            draw_text(screen, self.fonts, "Aguardando ação do oponente...", SCREEN_CONFIG.width // 2, 560, color=colors.WHITE, font=self.fonts.large, center=True)
            controls["leave"] = pygame.Rect(620, 20, 140, 38)
            draw_styled_button(screen, self.fonts, "Sair", controls["leave"], bg_color=colors.GRAY, hover_color=colors.GRAY, mouse_pos=mouse_pos, font=self.fonts.normal)
            return controls
        if switch_mode:
            controls["team"] = self._draw_team_choices(screen, player, mouse_pos)
            controls["back"] = pygame.Rect(560, 560, 160, 42)
            draw_styled_button(screen, self.fonts, "Cancelar", controls["back"], bg_color=colors.GRAY, hover_color=colors.GRAY, mouse_pos=mouse_pos, font=self.fonts.normal)
            return controls
        actions = [
            ("basic", "Ataque Básico"),
            ("special", "Ataque Especial"),
            ("heal", "Poção"),
            ("switch", "Trocar"),
            ("leave", "Sair"),
        ]
        for index, (key, label) in enumerate(actions):
            x = 60 + (index % 3) * 230
            y = 525 + (index // 3) * 50
            rect = pygame.Rect(x, y, 190, 40)
            bg = colors.GRAY if key == "leave" else colors.BATTLE_BUTTON_NORMAL
            hover = colors.GRAY if key == "leave" else colors.BATTLE_BUTTON_HOVER
            draw_styled_button(screen, self.fonts, label, rect, bg_color=bg, hover_color=hover, mouse_pos=mouse_pos, font=self.fonts.normal)
            controls[key] = rect
        return controls

    def _draw_header(self, screen: pygame.Surface, match: MatchSnapshot, player_id: str):
        turn = "sua vez" if match.active_player_id == player_id else "vez do oponente"
        draw_text(screen, self.fonts, f"Batalha Online - turno {match.turn_number} ({turn})", SCREEN_CONFIG.width // 2, 30, color=colors.WHITE, font=self.fonts.large, center=True)

    def _draw_pokemon_card(self, screen: pygame.Surface, player: PlayerSnapshot, rect: pygame.Rect, title: str):
        pokemon = self._active_pokemon(player)
        draw_rounded_box(screen, rect, colors.BATTLE_MENU_BG, radius=15, shadow_color=colors.SHADOW_COLOR_DARK, shadow_offset=(4, 4))
        pygame.draw.rect(screen, colors.BATTLE_MENU_BORDER, rect, 2, border_radius=15)
        draw_text(screen, self.fonts, f"{title}: {player.player_name}", rect.x + 18, rect.y + 16, color=colors.BLACK, font=self.fonts.normal)
        if pokemon is None:
            draw_text(screen, self.fonts, "Sem Pokémon", rect.centerx, rect.centery, color=colors.RED, font=self.fonts.large, center=True)
            return
        draw_text(screen, self.fonts, f"{pokemon.name} Nv {pokemon.level}", rect.x + 18, rect.y + 50, color=colors.DARK_BLUE, font=self.fonts.large)
        hp_text = f"HP {pokemon.hp}/{pokemon.max_hp}"
        draw_text(screen, self.fonts, hp_text, rect.x + 18, rect.y + 88, color=colors.BLACK, font=self.fonts.normal)
        bar_x = rect.x + 18
        bar_y = rect.y + 118
        bar_width = rect.width - 36
        ratio = 0 if pokemon.max_hp <= 0 else max(0, min(1, pokemon.hp / pokemon.max_hp))
        pygame.draw.rect(screen, colors.LIGHT_GRAY, (bar_x, bar_y, bar_width, 12), border_radius=6)
        pygame.draw.rect(screen, colors.GREEN, (bar_x, bar_y, int(bar_width * ratio), 12), border_radius=6)

    def _draw_events(self, screen: pygame.Surface, match: MatchSnapshot):
        panel = pygame.Rect(60, 285, 320, 195)
        draw_rounded_box(screen, panel, (238, 244, 252), radius=12, shadow_color=colors.SHADOW_COLOR_DARK, shadow_offset=(3, 3))
        pygame.draw.rect(screen, colors.BATTLE_MENU_BORDER, panel, 1, border_radius=12)
        draw_text(screen, self.fonts, "Eventos", panel.x + 15, panel.y + 12, color=colors.DARK_BLUE, font=self.fonts.normal)
        for index, event in enumerate(match.events[-5:]):
            draw_text(screen, self.fonts, event[:44], panel.x + 15, panel.y + 45 + index * 28, color=colors.BLACK, font=self.fonts.small)

    def _draw_team_choices(self, screen: pygame.Surface, player: PlayerSnapshot, mouse_pos) -> list[tuple[pygame.Rect, int]]:
        draw_text(screen, self.fonts, "Escolha o Pokémon para trocar", SCREEN_CONFIG.width // 2, 505, color=colors.WHITE, font=self.fonts.large, center=True)
        buttons = []
        for index, pokemon in enumerate(player.team):
            rect = pygame.Rect(70 + index * 220, 545, 190, 42)
            disabled = pokemon.hp <= 0 or index == player.active_pokemon_index
            bg = colors.LIGHT_GRAY if disabled else colors.BATTLE_BUTTON_NORMAL
            hover = colors.LIGHT_GRAY if disabled else colors.BATTLE_BUTTON_HOVER
            label = f"{pokemon.name} {pokemon.hp}/{pokemon.max_hp}"
            draw_styled_button(screen, self.fonts, label, rect, bg_color=bg, hover_color=hover, mouse_pos=mouse_pos, font=self.fonts.small)
            if not disabled:
                buttons.append((rect, index))
        return buttons

    def _find_player(self, match: MatchSnapshot, player_id: str) -> PlayerSnapshot | None:
        return next((player for player in match.players if player.player_id == player_id), None)

    def _find_opponent(self, match: MatchSnapshot, player_id: str) -> PlayerSnapshot | None:
        return next((player for player in match.players if player.player_id != player_id), None)

    def _active_pokemon(self, player: PlayerSnapshot):
        if not player.team:
            return None
        index = max(0, min(player.active_pokemon_index, len(player.team) - 1))
        return player.team[index]
