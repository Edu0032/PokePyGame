import pygame

from PokePY.config import LEADERBOARD_CONFIG


class GameOverState:
    def update(self, game, current_time_ms: int, current_time_seconds: float) -> None:
        game.game_over_view.draw(game.screen)
        pygame.display.flip()
        pygame.time.wait(1500)
        game.finish_failed_run()


class LeaderboardState:
    def update(self, game, current_time_ms: int, current_time_seconds: float) -> None:
        entries = game.leaderboard_service.top_scores(LEADERBOARD_CONFIG.display_limit)
        action = game.leaderboard_view.show(game.screen, entries, game.leaderboard_title, game.leaderboard_subtitle, game.leaderboard_footer)
        if action == "restart":
            game.restart_game()
        elif game.game_finished:
            game.credits.show(game.screen)
        else:
            game.close()
