import pygame

from PokePY.config import BATTLE_CONFIG, SCREEN_CONFIG
from PokePY.data.pokemon_catalog import BOSS_NAME
from PokePY.domain.game_state import BattleResult
from PokePY.domain.models import Player, Pokemon
from PokePY.infrastructure.assets import AssetLoader
from PokePY.services.battle_engine import BattleEngine
from PokePY.ui import colors
from PokePY.ui.fonts import FontBook
from PokePY.ui.widgets import draw_rounded_box, draw_styled_button, draw_text, is_button_clicked

class BattleView:
    def __init__(self, fonts: FontBook, assets: AssetLoader):
        self.fonts = fonts
        self.assets = assets

    def draw_pokemon_status(self, screen: pygame.Surface, pokemon: Pokemon, x_start: int, is_player: bool):
        box_width = 200
        box_height = 100
        box_y = SCREEN_CONFIG.height - 350 if is_player else 30
        status_rect = pygame.Rect(x_start, box_y, box_width, box_height)
        draw_rounded_box(screen, status_rect, colors.BATTLE_MENU_BG, radius=10, shadow_color=colors.SHADOW_COLOR_DARK, shadow_offset=(3, 3))
        draw_text(screen, self.fonts, pokemon.name, x_start + 10, box_y + 10, color=colors.BLACK, font=self.fonts.large)
        draw_text(screen, self.fonts, f"Lvl: {pokemon.level}", x_start + 10, box_y + 35, color=colors.BLACK)
        hp_bar_x = x_start + 10
        hp_bar_y = box_y + 60
        hp_bar_width = box_width - 20
        hp_bar_height = 15
        hp_ratio = pokemon.hp / pokemon.max_hp if pokemon.max_hp > 0 else 0
        hp_color = colors.HP_BAR_FULL
        if hp_ratio < 0.2:
            hp_color = colors.HP_BAR_EMPTY
        elif hp_ratio < 0.5:
            hp_color = colors.HP_BAR_LOW
        elif hp_ratio < 0.75:
            hp_color = colors.HP_BAR_MEDIUM
        pygame.draw.rect(screen, colors.HP_BAR_EMPTY, (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height), border_radius=5)
        pygame.draw.rect(screen, hp_color, (hp_bar_x, hp_bar_y, int(hp_bar_width * hp_ratio), hp_bar_height), border_radius=5)
        pygame.draw.rect(screen, colors.BLACK, (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height), 1, border_radius=5)
        draw_text(screen, self.fonts, f"HP: {pokemon.hp}/{pokemon.max_hp}", x_start + 10, box_y + 80, color=colors.BLACK)
        sprite_x = SCREEN_CONFIG.width * 0.2 if is_player else SCREEN_CONFIG.width * 0.8
        sprite_y = SCREEN_CONFIG.height * 0.3 if is_player else SCREEN_CONFIG.height * 0.32
        direction = "back" if is_player else "front"
        sprite = self.assets.load_sprite(pokemon.name, direction=direction)
        if sprite:
            screen.blit(sprite, (sprite_x - sprite.get_width() // 2, sprite_y - sprite.get_height() // 2))
        else:
            sprite_color = colors.BLUE if is_player else colors.RED
            pygame.draw.circle(screen, sprite_color, (int(sprite_x), int(sprite_y)), 50)
            draw_text(screen, self.fonts, "SPRITE", int(sprite_x) - 30, int(sprite_y) - 10, color=colors.WHITE)

    def draw_battle_screen(self, screen: pygame.Surface, current_pokemon: Pokemon, enemy: Pokemon, zone_name: str):
        background = self.assets.load_battle_background(zone_name)
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(colors.DARK_GREEN)
        overlay = pygame.Surface((SCREEN_CONFIG.width, SCREEN_CONFIG.height), pygame.SRCALPHA)
        overlay.fill(colors.BATTLE_BG_OVERLAY)
        screen.blit(overlay, (0, 0))
        self.draw_pokemon_status(screen, enemy, SCREEN_CONFIG.width - 250, is_player=False)
        self.draw_pokemon_status(screen, current_pokemon, 50, is_player=True)
        menu_rect = pygame.Rect(20, SCREEN_CONFIG.height - 170, SCREEN_CONFIG.width - 40, 150)
        draw_rounded_box(screen, menu_rect, colors.BATTLE_MENU_BG, radius=15, shadow_color=colors.SHADOW_COLOR_DARK, shadow_offset=(5, 5))
        pygame.draw.rect(screen, colors.BATTLE_MENU_BORDER, menu_rect, 2, border_radius=15)

    def display_message(self, screen: pygame.Surface, current_pokemon: Pokemon, enemy: Pokemon, message: str, zone_name: str, wait_time: int = 1500):
        self.draw_battle_screen(screen, current_pokemon, enemy, zone_name)
        message_rect = pygame.Rect(40, SCREEN_CONFIG.height - 150, SCREEN_CONFIG.width - 80, 50)
        pygame.draw.rect(screen, colors.WHITE, message_rect, border_radius=10)
        pygame.draw.rect(screen, colors.BATTLE_MENU_BORDER, message_rect, 2, border_radius=10)
        draw_text(screen, self.fonts, message, message_rect.centerx, message_rect.centery, color=colors.BLACK, font=self.fonts.large, center=True)
        pygame.display.flip()
        if wait_time > 0:
            pygame.time.wait(wait_time)

    def draw_action_buttons(self, screen: pygame.Surface, labels: list[str], mouse_pos) -> list[tuple[pygame.Rect, int]]:
        menu_x = 20
        menu_y = SCREEN_CONFIG.height - 170
        menu_width = SCREEN_CONFIG.width - 40
        menu_height = 150
        button_width = menu_width / 2 - 15
        button_height = menu_height / 2 - 15
        keys = ["Z", "X", "C", "V"]
        positions = [
            (menu_x + 10, menu_y + 10),
            (menu_x + 10 + button_width + 10, menu_y + 10),
            (menu_x + 10, menu_y + 10 + button_height + 10),
            (menu_x + 10 + button_width + 10, menu_y + 10 + button_height + 10),
        ]
        buttons = []
        for index, label in enumerate(labels):
            x, y = positions[index]
            rect = pygame.Rect(x, y, button_width, button_height)
            bg = colors.GRAY if label == "Voltar" else colors.BATTLE_BUTTON_NORMAL
            hover = colors.GRAY if label == "Voltar" else colors.BATTLE_BUTTON_HOVER
            draw_styled_button(screen, self.fonts, f"[{keys[index]}] {label}", rect, colors.BLACK, bg, hover, mouse_pos=mouse_pos, font=self.fonts.large)
            buttons.append((rect, index))
        return buttons

class BattleController:
    def __init__(self, view: BattleView, engine: BattleEngine):
        self.view = view
        self.engine = engine
        self.clock = pygame.time.Clock()

    def run_battle(self, screen: pygame.Surface, player: Player, current_pokemon: Pokemon, enemy: Pokemon, zone_name: str) -> BattleResult:
        if not current_pokemon.is_alive():
            return BattleResult.SWITCH_REQUIRED
        turn = "player"
        battle_state = "main_menu"
        while current_pokemon.is_alive() and enemy.is_alive():
            mouse_pos = pygame.mouse.get_pos()
            self.view.draw_battle_screen(screen, current_pokemon, enemy, zone_name)
            if turn == "player":
                if battle_state == "main_menu":
                    self.view.display_message(screen, current_pokemon, enemy, f"O que {current_pokemon.name} fará?", zone_name, wait_time=0)
                    buttons = self.view.draw_action_buttons(screen, ["Lutar", "Cura", "Trocar", "Fugir"], mouse_pos)
                else:
                    self.view.display_message(screen, current_pokemon, enemy, "Escolha um ataque:", zone_name, wait_time=0)
                    buttons = self.view.draw_action_buttons(screen, ["Ataque Básico", "Ataque Especial", "Voltar"], mouse_pos)
                pygame.display.flip()
                action = self._wait_for_action(buttons)
                if action is None:
                    continue
                if battle_state == "main_menu":
                    result = self._handle_main_action(screen, player, current_pokemon, enemy, zone_name, action)
                    if result in {BattleResult.FLED, BattleResult.FLEE_BLOCKED, BattleResult.SWITCH_REQUESTED}:
                        return result
                    if result == "attack_menu":
                        battle_state = "attack_menu"
                    elif result == "enemy_turn":
                        turn = "enemy"
                else:
                    if action == 2:
                        battle_state = "main_menu"
                    else:
                        attack_name, damage = self.engine.player_attack(current_pokemon, enemy, action)
                        self.view.display_message(screen, current_pokemon, enemy, f"{current_pokemon.name} usou {attack_name}! Dano: {damage}", zone_name, 1500)
                        if not enemy.is_alive():
                            self.engine.reward_victory(current_pokemon, enemy)
                            self.view.display_message(screen, current_pokemon, enemy, f"{enemy.name} desmaiou! {current_pokemon.name} ganhou XP!", zone_name, 2000)
                            return BattleResult.WIN
                        battle_state = "main_menu"
                        turn = "enemy"
            else:
                damage = self.engine.enemy_attack(enemy, current_pokemon)
                self.view.display_message(screen, current_pokemon, enemy, f"{enemy.name} atacou! Dano recebido: {damage}", zone_name, 1500)
                if not current_pokemon.is_alive():
                    self.view.display_message(screen, current_pokemon, enemy, f"Seu Pokémon {current_pokemon.name} desmaiou!", zone_name, 1000)
                    return BattleResult.SWITCH_REQUIRED if player.has_alive_pokemon() else BattleResult.LOSE
                turn = "player"
            self.clock.tick(SCREEN_CONFIG.fps)
        if current_pokemon.is_alive():
            self.engine.reward_victory(current_pokemon, enemy)
            return BattleResult.WIN
        return BattleResult.LOSE

    def select_pokemon_in_battle(self, screen: pygame.Surface, player: Player, current_pokemon: Pokemon | None, enemy: Pokemon, zone_name: str) -> tuple[Pokemon | None, bool]:
        while True:
            candidate_buttons = []
            self.view.draw_battle_screen(screen, current_pokemon or player.first_alive_pokemon(), enemy, zone_name)
            panel = pygame.Rect(170, 130, 460, 380)
            draw_rounded_box(screen, panel, colors.BATTLE_MENU_BG, radius=15, shadow_color=colors.SHADOW_COLOR_DARK, shadow_offset=(5, 5))
            pygame.draw.rect(screen, colors.BATTLE_MENU_BORDER, panel, 2, border_radius=15)
            draw_text(screen, self.view.fonts, "Escolha seu Pokémon", panel.centerx, panel.y + 35, color=colors.BLACK, font=self.view.fonts.xl, center=True)
            mouse_pos = pygame.mouse.get_pos()
            for index, pokemon in enumerate(player.team):
                y = panel.y + 80 + index * 70
                disabled = not pokemon.is_alive() or pokemon is current_pokemon
                label = f"{pokemon.name}  HP {pokemon.hp}/{pokemon.max_hp}  Nv {pokemon.level}"
                rect = pygame.Rect(panel.x + 35, y, panel.width - 70, 50)
                bg = colors.LIGHT_GRAY if disabled else colors.BATTLE_BUTTON_NORMAL
                hover = colors.LIGHT_GRAY if disabled else colors.BATTLE_BUTTON_HOVER
                draw_styled_button(screen, self.view.fonts, label, rect, colors.BLACK, bg, hover, mouse_pos=mouse_pos, font=self.view.fonts.normal)
                candidate_buttons.append((rect, pokemon, disabled))
            back_rect = pygame.Rect(panel.x + 35, panel.bottom - 65, panel.width - 70, 45)
            if current_pokemon and current_pokemon.is_alive():
                draw_styled_button(screen, self.view.fonts, "Voltar", back_rect, colors.BLACK, colors.GRAY, colors.GRAY, mouse_pos=mouse_pos)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = pygame.mouse.get_pos()
                    if current_pokemon and current_pokemon.is_alive() and is_button_clicked(click_pos, back_rect):
                        return current_pokemon, False
                    for rect, pokemon, disabled in candidate_buttons:
                        if not disabled and is_button_clicked(click_pos, rect):
                            return pokemon, True
            self.clock.tick(SCREEN_CONFIG.fps)

    def _wait_for_action(self, buttons: list[tuple[pygame.Rect, int]]) -> int | None:
        key_map = {pygame.K_z: 0, pygame.K_x: 1, pygame.K_c: 2, pygame.K_v: 3}
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for rect, index in buttons:
                        if is_button_clicked(mouse_pos, rect):
                            return index
                if event.type == pygame.KEYDOWN and event.key in key_map:
                    index = key_map[event.key]
                    if index < len(buttons):
                        return index
            self.clock.tick(SCREEN_CONFIG.fps)

    def _handle_main_action(self, screen: pygame.Surface, player: Player, current_pokemon: Pokemon, enemy: Pokemon, zone_name: str, action_index: int):
        if action_index == 0:
            return "attack_menu"
        if action_index == 1:
            if self.engine.heal_active_pokemon(player, current_pokemon):
                self.view.display_message(screen, current_pokemon, enemy, f"{current_pokemon.name} foi curado!", zone_name, 1000)
                return "enemy_turn"
            self.view.display_message(screen, current_pokemon, enemy, "Sem Poções!", zone_name, 1000)
            return None
        if action_index == 2:
            return BattleResult.SWITCH_REQUESTED
        flee_result = self.engine.try_flee(enemy)
        if flee_result == BattleResult.FLED:
            return BattleResult.FLED
        if flee_result == BattleResult.FLEE_BLOCKED:
            self.view.display_message(screen, current_pokemon, enemy, "Você não pode fugir da Batalha Final!", zone_name, 1000)
            return BattleResult.FLEE_BLOCKED
        self.view.display_message(screen, current_pokemon, enemy, "Fuga falhou!", zone_name, 1000)
        return "enemy_turn"
