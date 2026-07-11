import pygame

from PokePY.data.pokemon_catalog import BOSS_NAME
from PokePY.domain.game_state import BattleResult, GameState
from PokePY.ui import colors
from PokePY.ui.widgets import draw_modal_message, draw_text


class BattleState:
    def update(self, game, current_time_ms: int, current_time_seconds: float) -> None:
        result = game.battle_controller.run_battle(
            game.screen,
            game.player,
            game.current_battle_pokemon,
            game.current_enemy,
            game.current_zone.name,
            game.story_battle_charge,
        )
        if result == BattleResult.WIN:
            self._handle_win(game)
        elif result == BattleResult.LOSE:
            game.story_battle_charge.reset()
            game.state = GameState.GAME_OVER
        elif result == BattleResult.FLED:
            game.story_battle_charge.reset()
            draw_modal_message(game.screen, game.fonts, "Você fugiu com sucesso!")
            pygame.display.flip()
            pygame.time.wait(1500)
            game.state = GameState.EXPLORE
        elif result == BattleResult.FLEE_BLOCKED:
            draw_modal_message(
                game.screen,
                game.fonts,
                "Não é possível fugir do Boss!",
                bg_color=colors.CONFIRM_COLOR_BAD,
                border_color=colors.RED,
                text_color=colors.TEXT_COLOR_LIGHT,
            )
            pygame.display.flip()
            pygame.time.wait(1500)
            game.state = GameState.BATTLE
        elif result in {BattleResult.SWITCH_REQUIRED, BattleResult.SWITCH_REQUESTED}:
            game.state = GameState.SELECT_IN_BATTLE

    def _handle_win(self, game) -> None:
        game.story_battle_charge.reset()
        if game.current_enemy.name == BOSS_NAME:
            game.final_boss_defeated = True
            draw_text(
                game.screen,
                game.fonts,
                "O Boss Final foi derrotado!",
                200,
                300,
                color=colors.GREEN,
                font=game.fonts.xl,
            )
            pygame.display.flip()
            pygame.time.wait(2000)
            game.save_progress()
            game.complete_game()
            return
        game.save_progress()
        draw_text(game.screen, game.fonts, "Você venceu e ganhou XP!", 300, 300)
        pygame.display.flip()
        pygame.time.wait(1000)
        game.state = GameState.EXPLORE


class PokemonSwitchState:
    def update(self, game, current_time_ms: int, current_time_seconds: float) -> None:
        forced_switch = not game.current_battle_pokemon.is_alive()
        current = game.current_battle_pokemon if not forced_switch else None
        new_pokemon, switched = game.battle_controller.select_pokemon_in_battle(
            game.screen,
            game.player,
            current,
            game.current_enemy,
            game.current_zone.name,
        )
        if switched:
            game.current_battle_pokemon = new_pokemon
            game.battle_view.display_message(
                game.screen,
                game.current_battle_pokemon,
                game.current_enemy,
                f"Vai, {game.current_battle_pokemon.name}!",
                game.current_zone.name,
                1000,
            )
            game.state = GameState.BATTLE
        elif not switched and not forced_switch:
            game.state = GameState.BATTLE
