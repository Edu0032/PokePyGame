import pygame

from PokePY.config import ITEM_CONFIG, PLAYER_CONFIG, SCREEN_CONFIG, WORLD_CONFIG
from PokePY.data.pokemon_catalog import BOSS_NAME
from PokePY.data.zones import ZONE_DEFINITIONS
from PokePY.domain.game_state import GameState
from PokePY.game.states.leaderboard_state import open_ranking
from PokePY.game.states.multiplayer_state import start_multiplayer_lobby
from PokePY.ui.widgets import is_button_clicked


class ExplorationState:
    def update(self, game, current_time_ms: int, current_time_seconds: float) -> None:
        game.exploration_view.draw_map(game.screen, game.current_zone.name)
        moved = self._move_player(game)
        sprite = game.sprite_animator.update(current_time_ms, moved)
        game.exploration_view.draw_player(game.screen, game.player, sprite)
        game.exploration_view.draw_hud(
            game.screen,
            game.player,
            game.current_zone.name,
            current_time_ms,
        )
        self._draw_timer(game)
        button_center, button_radius = game.exploration_view.draw_backpack_button(game.screen)
        multiplayer_button = game.exploration_view.draw_multiplayer_button(game.screen)
        ranking_button = game.exploration_view.draw_ranking_button(game.screen)
        self._handle_events(
            game,
            button_center,
            button_radius,
            multiplayer_button,
            ranking_button,
        )
        if game.state != GameState.EXPLORE:
            return
        if self._try_start_final_boss(game):
            return
        if self._try_random_grass_event(
            game,
            moved,
            current_time_ms,
            current_time_seconds,
        ):
            return
        self._try_change_zone(game)
        game.item_message = game.exploration_view.draw_item_message(
            game.screen,
            game.item_message,
            game.item_message_timer_ms,
            current_time_ms,
        )

    def _draw_timer(self, game) -> None:
        if game.session.started_at is not None:
            game.timer_view.draw(game.screen, game.session.elapsed_seconds)

    def _move_player(self, game) -> bool:
        keys = pygame.key.get_pressed()
        moved = False
        if keys[pygame.K_LEFT]:
            game.player.x -= PLAYER_CONFIG.move_speed
            game.sprite_animator.direction = "Esquerda"
            moved = True
        elif keys[pygame.K_RIGHT]:
            game.player.x += PLAYER_CONFIG.move_speed
            game.sprite_animator.direction = "Direita"
            moved = True
        elif keys[pygame.K_UP]:
            game.player.y -= PLAYER_CONFIG.move_speed
            game.sprite_animator.direction = "Costas"
            moved = True
        elif keys[pygame.K_DOWN]:
            game.player.y += PLAYER_CONFIG.move_speed
            game.sprite_animator.direction = "Frente"
            moved = True
        game.player.x = max(
            PLAYER_CONFIG.boundary_padding,
            min(game.player.x, SCREEN_CONFIG.width - PLAYER_CONFIG.boundary_padding),
        )
        game.player.y = max(
            PLAYER_CONFIG.boundary_padding,
            min(game.player.y, SCREEN_CONFIG.height - PLAYER_CONFIG.boundary_padding),
        )
        return moved

    def _handle_events(
        self,
        game,
        button_center,
        button_radius: int,
        multiplayer_button,
        ranking_button,
    ) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    start_multiplayer_lobby(game)
                elif event.key == pygame.K_r:
                    open_ranking(game)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if game.exploration_view.click_hits_backpack(
                    mouse_pos,
                    button_center,
                    button_radius,
                ):
                    game.state = GameState.INVENTORY
                    game.inventory_full_flag = False
                elif is_button_clicked(mouse_pos, multiplayer_button):
                    start_multiplayer_lobby(game)
                elif is_button_clicked(mouse_pos, ranking_button):
                    open_ranking(game)

    def _try_start_final_boss(self, game) -> bool:
        if game.current_zone.name != "Zona 3" or game.final_boss_defeated or game.final_boss_triggered:
            return False
        inside_boss_path = (
            SCREEN_CONFIG.height // 2 - WORLD_CONFIG.boss_path_half_height
            < game.player.y
            < SCREEN_CONFIG.height // 2 + WORLD_CONFIG.boss_path_half_height
        )
        near_exit = game.player.x > SCREEN_CONFIG.width - WORLD_CONFIG.boss_trigger_distance_from_right
        if not (inside_boss_path and near_exit):
            return False
        game.final_boss_triggered = True
        game.current_battle_pokemon = game.player.first_alive_pokemon()
        if game.current_battle_pokemon is None:
            game.state = GameState.GAME_OVER
            return True
        game.fade_message("Um inimigo colossal bloqueia o caminho!")
        game.current_enemy = game.pokemon_factory.create(
            BOSS_NAME,
            "Gelo",
            level=10,
            hp=400,
        )
        game.story_battle_charge.reset()
        game.state = GameState.BATTLE
        return True

    def _try_random_grass_event(
        self,
        game,
        moved: bool,
        current_time_ms: int,
        current_time_seconds: float,
    ) -> bool:
        if not moved:
            return False
        if game.current_zone.name == "Zona 3" and game.final_boss_triggered:
            return False
        if not game.map_mask.is_in_grass(
            game.current_zone.name,
            game.player.x,
            game.player.y,
        ):
            return False
        if not game.player.repel_active:
            enemy = game.encounters.random_encounter(game.current_zone)
            if enemy:
                game.current_enemy = enemy
                game.current_battle_pokemon = game.player.first_alive_pokemon()
                game.story_battle_charge.reset()
                game.state = GameState.BATTLE if game.current_battle_pokemon else GameState.GAME_OVER
                return True
        if current_time_seconds - game.last_item_pickup_time >= ITEM_CONFIG.pickup_cooldown_seconds:
            item = game.encounters.random_item(
                game.current_zone,
                game.player.x,
                SCREEN_CONFIG.width,
                WORLD_CONFIG.boss_trigger_distance_from_right,
            )
            if item:
                self._collect_item(
                    game,
                    item,
                    current_time_ms,
                    current_time_seconds,
                )
        return False

    def _collect_item(
        self,
        game,
        item: str,
        current_time_ms: int,
        current_time_seconds: float,
    ) -> None:
        if game.player.add_item(item):
            game.item_message = f"Encontrou {item}!"
            game.item_message_timer_ms = current_time_ms + ITEM_CONFIG.message_duration_ms
            game.last_item_pickup_time = current_time_seconds
            game.inventory_full_flag = False
            game.save_progress()
        elif not game.inventory_full_flag:
            game.item_message = f"Inventário de {item} cheio!"
            game.item_message_timer_ms = current_time_ms + ITEM_CONFIG.message_duration_ms
            game.inventory_full_flag = True

    def _try_change_zone(self, game) -> None:
        if game.player.x <= WORLD_CONFIG.transition_edge_x:
            return
        game.player.zone_index += 1
        next_index = game.current_zone_index + 1
        if next_index < len(ZONE_DEFINITIONS):
            game.fade_transition(f"Indo para {ZONE_DEFINITIONS[next_index].name}...")
            game.current_zone_index = next_index
            game.player.x = WORLD_CONFIG.zone_entry_x
            game.fade_in()
            game.save_progress()
            return
        game.player.x = WORLD_CONFIG.blocked_entry_x
        game.fade_message("Derrote o Boss Final para zerar o jogo!")
