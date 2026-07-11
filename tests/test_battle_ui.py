import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame
from PokePY.config import SCREEN_CONFIG
from PokePY.services.battle_engine import BattleEngine
from PokePY.services.combat_rules import BattleChargeTracker
from PokePY.ui.battle import BattleController, BattleView
from PokePY.ui.fonts import FontBook


class EmptyAssets:
    def load_battle_background(self, zone_name):
        return None

    def load_sprite(self, pokemon_name, direction="front", scale=2):
        return None


def test_message_box_does_not_overlap_action_menu():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_CONFIG.width, SCREEN_CONFIG.height))
    view = BattleView(FontBook(), EmptyAssets())
    message = view.draw_message_box(screen, "Mensagem")
    action_menu_top = SCREEN_CONFIG.height - 170
    assert message.bottom < action_menu_top
    pygame.quit()


def test_only_special_is_available_after_two_normal_attacks():
    controller = BattleController.__new__(BattleController)
    controller.engine = BattleEngine()
    controller.clock = pygame.time.Clock()
    normal = controller._attack_options(BattleChargeTracker(1))
    special = controller._attack_options(BattleChargeTracker(2))
    assert normal[0] == (0, "Ataque Básico")
    assert special[0] == (1, "Ataque Especial")
