import pygame

from PokePY.config import SCREEN_CONFIG, UI_CONFIG
from PokePY.domain.game_state import GameState
from PokePY.ui.widgets import draw_text, is_button_clicked


class InventoryState:
    def update(self, game, current_time_ms: int, current_time_seconds: float) -> None:
        repel_button, potion_button, close_button = game.inventory_view.draw(game.screen, game.player)
        box_y = (SCREEN_CONFIG.height - UI_CONFIG.inventory_height) // 2
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.close()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if is_button_clicked(mouse_pos, repel_button):
                    self._use_repel(game, box_y)
                elif is_button_clicked(mouse_pos, potion_button):
                    self._use_potion(game, box_y)
                elif is_button_clicked(mouse_pos, close_button):
                    game.state = GameState.EXPLORE

    def _use_repel(self, game, box_y: int) -> None:
        if game.player.use_item("Repelente"):
            message = "Repelente ativado!"
            color = (50, 50, 80)
            game.save_progress()
        else:
            message = "Sem Repelentes!"
            color = (200, 60, 60)
        draw_text(
            game.screen,
            game.fonts,
            message,
            SCREEN_CONFIG.width // 2,
            box_y + UI_CONFIG.inventory_height - 40,
            color=color,
            font=game.fonts.large,
            center=True,
        )
        pygame.display.flip()
        pygame.time.wait(1000)

    def _use_potion(self, game, box_y: int) -> None:
        if game.player.items.get("Poção", 0) > 0:
            result = game.inventory_view.select_pokemon_for_heal(game.screen, game.player)
            if result in {"healed", "canceled"}:
                if result == "healed":
                    game.save_progress()
                game.state = GameState.INVENTORY
            return
        draw_text(
            game.screen,
            game.fonts,
            "Sem Poções!",
            SCREEN_CONFIG.width // 2,
            box_y + UI_CONFIG.inventory_height - 40,
            color=(200, 60, 60),
            font=game.fonts.large,
            center=True,
        )
        pygame.display.flip()
        pygame.time.wait(1000)
