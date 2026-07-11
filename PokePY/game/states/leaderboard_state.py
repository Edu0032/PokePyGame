import pygame

from PokePY.config import LEADERBOARD_CONFIG
from PokePY.domain.game_state import GameState
from PokePY.ui.widgets import is_button_clicked


def open_ranking(game) -> None:
    game.ranking_entries = []
    game.ranking_error = None
    game.ranking_loaded = False
    game.state = GameState.RANKING


class GameOverState:
    def update(self, game, current_time_ms: int, current_time_seconds: float) -> None:
        game.game_over_view.draw(game.screen)
        pygame.display.flip()
        pygame.time.wait(1500)
        game.finish_failed_run()


class LeaderboardState:
    def update(self, game, current_time_ms: int, current_time_seconds: float) -> None:
        try:
            entries = game.leaderboard_service.top_scores(LEADERBOARD_CONFIG.display_limit)
        except Exception as error:
            print(f"[PokePY ranking] Falha ao carregar ranking: {error}")
            entries = []
        action = game.leaderboard_view.show(
            game.screen,
            entries,
            game.leaderboard_title,
            game.leaderboard_subtitle,
            game.leaderboard_footer,
        )
        if action == "restart":
            game.restart_game()
        elif game.game_finished:
            game.credits.show(game.screen)
        else:
            game.close()


class RankingBrowserState:
    def update(self, game, current_time_ms: int, current_time_seconds: float) -> None:
        if not game.ranking_loaded:
            game.ranking_loaded = True
            try:
                game.ranking_entries = game.leaderboard_service.top_scores(LEADERBOARD_CONFIG.display_limit)
                game.ranking_error = None
            except Exception as error:
                game.ranking_entries = []
                game.ranking_error = "Não foi possível carregar o ranking online. Tente novamente."
                print(f"[PokePY ranking] Falha ao carregar ranking: {error}")
        back_button = game.leaderboard_view.draw_browser(
            game.screen,
            game.ranking_entries,
            game.ranking_error,
            pygame.mouse.get_pos(),
        )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.close()
            if (
                event.type == pygame.KEYDOWN
                and event.key
                in {
                    pygame.K_ESCAPE,
                    pygame.K_q,
                    pygame.K_r,
                }
                or event.type == pygame.MOUSEBUTTONDOWN
                and is_button_clicked(
                    pygame.mouse.get_pos(),
                    back_button,
                )
            ):
                game.state = GameState.EXPLORE
