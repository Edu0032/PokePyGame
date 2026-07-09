import pygame

from PokePY.config import PLAYER_CONFIG
from PokePY.domain.game_state import GameState


class TeamSelectionState:
    def update(self, game, current_time_ms: int, current_time_seconds: float) -> None:
        buttons, confirm_button = game.team_view.draw(game.screen, game.selected_pokemon)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.close()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button_rect, pokemon in buttons:
                    if button_rect.collidepoint(mouse_pos):
                        self._toggle_selected_pokemon(game, pokemon)
                if confirm_button.collidepoint(mouse_pos) and len(game.selected_pokemon) == PLAYER_CONFIG.team_size:
                    game.player.team = [pokemon.clone() for pokemon in game.selected_pokemon]
                    game.session.start()
                    game.save_progress()
                    game.state = GameState.EXPLORE

    def _toggle_selected_pokemon(self, game, pokemon) -> None:
        selected_names = {selected.name for selected in game.selected_pokemon}
        if pokemon.name in selected_names:
            game.selected_pokemon = [selected for selected in game.selected_pokemon if selected.name != pokemon.name]
        elif len(game.selected_pokemon) < PLAYER_CONFIG.team_size:
            game.selected_pokemon.append(pokemon.clone())
