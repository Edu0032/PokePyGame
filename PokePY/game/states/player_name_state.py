import pygame

from PokePY.domain.game_state import GameState


class PlayerNameState:
    def update(self, game, current_time_ms: int, current_time_seconds: float) -> None:
        mouse_pos = pygame.mouse.get_pos()
        start_button = game.player_name_view.draw(game.screen, game.typed_player_name, mouse_pos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.close()
            if event.type == pygame.KEYDOWN:
                if game.player_name_view.should_start(event):
                    self._confirm_name(game)
                else:
                    game.typed_player_name = game.player_name_view.normalize_input(game.typed_player_name, event)
            if game.player_name_view.should_start(event, start_button):
                self._confirm_name(game)

    def _confirm_name(self, game) -> None:
        game.session.identify_player(game.typed_player_name.strip() or "Treinador")
        game.state = GameState.SELECT_TEAM
