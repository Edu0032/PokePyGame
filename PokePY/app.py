import sys
import time

import pygame

from PokePY.config import API_CONFIG, LEADERBOARD_CONFIG, PLAYER_CONFIG, SCREEN_CONFIG
from PokePY.data.zones import ZONE_DEFINITIONS
from PokePY.domain.factories import PokemonFactory
from PokePY.domain.game_state import GameState
from PokePY.domain.models import Player
from PokePY.domain.session import GameSession
from PokePY.game.state_machine import StateMachine
from PokePY.game.states import build_state_handlers
from PokePY.infrastructure.assets import AssetLoader
from PokePY.infrastructure.map_mask import MapMaskService
from PokePY.infrastructure.repository_factory import create_leaderboard_repository, create_multiplayer_gateway, create_player_progress_repository
from PokePY.services.battle_engine import BattleEngine
from PokePY.services.encounter_service import EncounterService
from PokePY.services.leaderboard_service import LeaderboardService
from PokePY.services.multiplayer_serialization import MultiplayerSerializer
from PokePY.services.player_progress_service import PlayerProgressService
from PokePY.services.time_formatter import format_seconds
from PokePY.ui import colors
from PokePY.ui.battle import BattleController, BattleView
from PokePY.ui.credits import CreditsScreen
from PokePY.ui.exploration import ExplorationView, PlayerSpriteAnimator
from PokePY.ui.fonts import FontBook
from PokePY.ui.game_over import GameOverView
from PokePY.ui.inventory import InventoryView
from PokePY.ui.leaderboard import LeaderboardView
from PokePY.ui.multiplayer import MultiplayerBattleView, MultiplayerLobbyView
from PokePY.ui.player_name import PlayerNameView
from PokePY.ui.team_selection import TeamSelectionView
from PokePY.ui.timer import RunTimerView
from PokePY.ui.widgets import draw_text


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_CONFIG.width, SCREEN_CONFIG.height))
        pygame.display.set_caption(SCREEN_CONFIG.title)
        self.clock = pygame.time.Clock()
        self.state_machine = StateMachine(build_state_handlers())
        self._load_core_dependencies()
        self._load_ui_dependencies()
        self._reset_runtime_state()

    @property
    def current_zone(self):
        return ZONE_DEFINITIONS[self.current_zone_index]

    def run(self) -> None:
        while True:
            current_time_ms = pygame.time.get_ticks()
            current_time_seconds = time.time()
            self.player.update_repel(current_time_ms)
            previous_state = self.state
            self.state_machine.update(self, current_time_ms, current_time_seconds)
            if previous_state == GameState.INVENTORY and self.state == GameState.EXPLORE:
                self.player.activate_pending_repel(current_time_ms)
            pygame.display.flip()
            self.clock.tick(SCREEN_CONFIG.fps)

    def complete_game(self) -> None:
        if not self.game_finished:
            self.session.finish()
            elapsed_text = format_seconds(self.session.elapsed_seconds)
            try:
                result = self.leaderboard_service.register_completion(self.session.player_name, self.session.elapsed_seconds)
                position_text = f"Posição no ranking: #{result.position}" if result.position else "Tempo salvo no ranking."
                self.leaderboard_subtitle = f"{self.session.player_name} zerou em {format_seconds(result.entry.elapsed_seconds)}. {position_text}"
            except Exception as error:
                self.leaderboard_subtitle = f"{self.session.player_name} zerou em {elapsed_text}, mas o ranking online não foi salvo. Verifique {API_CONFIG.base_url}/health/ready."
                print(f"[PokePY leaderboard] Falha ao salvar placar online: {error}")
            self.leaderboard_title = "Jogo concluído!"
            self.leaderboard_footer = "ENTER/R para jogar novamente ou ESC/Q para ver os créditos e sair"
            self.game_finished = True
        self.state = GameState.LEADERBOARD

    def finish_failed_run(self) -> None:
        self.session.finish()
        self.leaderboard_title = "Fim de tentativa"
        self.leaderboard_subtitle = f"Sua tentativa durou {format_seconds(self.session.elapsed_seconds)}. Só conclusões entram no ranking."
        self.leaderboard_footer = "ENTER/R para tentar novamente ou ESC/Q para sair"
        self.state = GameState.LEADERBOARD

    def restart_game(self) -> None:
        player_name = self.session.player_name
        typed_name = self.typed_player_name
        self._reset_runtime_state()
        self.session.identify_player(player_name)
        self.typed_player_name = typed_name
        self.state = GameState.SELECT_TEAM

    def save_progress(self) -> None:
        try:
            self.progress_service.save(self.session.player_id, self.player, self.session.player_name)
        except Exception:
            return

    def fade_message(self, message: str) -> None:
        for alpha in range(0, 300, 5):
            surface = pygame.Surface((SCREEN_CONFIG.width, SCREEN_CONFIG.height))
            surface.set_alpha(alpha)
            surface.fill(colors.BLACK)
            self.screen.blit(surface, (0, 0))
            draw_text(self.screen, self.fonts, message, 150, 280, color=colors.WHITE, font=self.fonts.xl)
            pygame.display.flip()
            pygame.time.wait(5)
        pygame.time.wait(1000)

    def fade_transition(self, message: str) -> None:
        for alpha in range(0, 255, 15):
            surface = pygame.Surface((SCREEN_CONFIG.width, SCREEN_CONFIG.height))
            surface.set_alpha(alpha)
            surface.fill(colors.BLACK)
            self.screen.blit(surface, (0, 0))
            if alpha > 100:
                draw_text(self.screen, self.fonts, message, SCREEN_CONFIG.width // 2, SCREEN_CONFIG.height // 2, color=colors.WHITE, font=self.fonts.xl, center=True)
            pygame.display.flip()
            pygame.time.wait(20)

    def fade_in(self) -> None:
        for alpha in range(255, 0, -15):
            self.exploration_view.draw_map(self.screen, self.current_zone.name)
            self.exploration_view.draw_player(self.screen, self.player, self.sprite_animator.last_valid_sprite)
            surface = pygame.Surface((SCREEN_CONFIG.width, SCREEN_CONFIG.height))
            surface.set_alpha(alpha)
            surface.fill(colors.BLACK)
            self.screen.blit(surface, (0, 0))
            pygame.display.flip()
            pygame.time.wait(20)

    def close(self) -> None:
        pygame.quit()
        sys.exit()

    def _load_core_dependencies(self) -> None:
        self.fonts = FontBook()
        self.assets = AssetLoader()
        self.pokemon_factory = PokemonFactory()
        self.pokemon_options = self.pokemon_factory.starter_options()
        self.leaderboard_service = LeaderboardService(create_leaderboard_repository())
        self.progress_service = PlayerProgressService(create_player_progress_repository())
        self.multiplayer_gateway = create_multiplayer_gateway()
        self.multiplayer_serializer = MultiplayerSerializer()
        self.encounters = EncounterService(self.pokemon_factory)
        self.map_mask = MapMaskService(self.assets)

    def _load_ui_dependencies(self) -> None:
        self.team_view = TeamSelectionView(self.fonts, self.pokemon_options)
        self.inventory_view = InventoryView(self.fonts, self.assets)
        self.exploration_view = ExplorationView(self.fonts, self.assets)
        self.sprite_animator = PlayerSpriteAnimator(self.assets)
        self.battle_view = BattleView(self.fonts, self.assets)
        self.battle_controller = BattleController(self.battle_view, BattleEngine())
        self.credits = CreditsScreen(self.fonts)
        self.player_name_view = PlayerNameView(self.fonts)
        self.leaderboard_view = LeaderboardView(self.fonts)
        self.game_over_view = GameOverView(self.fonts)
        self.timer_view = RunTimerView(self.fonts)
        self.multiplayer_lobby_view = MultiplayerLobbyView(self.fonts)
        self.multiplayer_battle_view = MultiplayerBattleView(self.fonts)

    def _reset_runtime_state(self) -> None:
        self.session = GameSession()
        self.player = Player()
        self.selected_pokemon = []
        self.typed_player_name = ""
        self.state = GameState.PLAYER_NAME
        self.current_zone_index = 0
        self.current_enemy = None
        self.current_battle_pokemon = None
        self.final_boss_defeated = False
        self.final_boss_triggered = False
        self.item_message = None
        self.item_message_timer_ms = 0
        self.last_item_pickup_time = 0.0
        self.inventory_full_flag = False
        self.multiplayer_ticket = None
        self.multiplayer_match = None
        self.multiplayer_error = None
        self.multiplayer_status_text = "Clique para entrar na fila online."
        self.multiplayer_last_poll_ms = 0
        self.multiplayer_switch_mode = False
        self.leaderboard_title = "Placar"
        self.leaderboard_subtitle = "Melhores tempos de conclusão"
        self.leaderboard_footer = "ENTER/R para jogar novamente ou ESC/Q para sair"
        self.game_finished = False
