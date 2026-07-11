import pygame

from PokePY.config import API_CONFIG, BATTLE_CONFIG
from PokePY.domain.game_state import GameState
from PokePY.services.multiplayer_contracts import (
    MatchStatus,
    MultiplayerAction,
    MultiplayerActionType,
)
from PokePY.ui.widgets import is_button_clicked


def start_multiplayer_lobby(game) -> None:
    if not game.player.team:
        game.multiplayer_error = "Escolha um time antes de entrar no multiplayer."
        game.state = GameState.EXPLORE
        return
    if not game.player.has_alive_pokemon():
        game.multiplayer_error = "Cure pelo menos um Pokémon antes de batalhar online."
        game.state = GameState.EXPLORE
        return
    game.save_progress()
    game.multiplayer_ticket = None
    game.multiplayer_match = None
    game.multiplayer_error = None
    game.multiplayer_status_text = "Clique para entrar na fila online."
    game.multiplayer_last_poll_ms = 0
    game.multiplayer_switch_mode = False
    game.state = GameState.MULTIPLAYER_LOBBY


class MultiplayerLobbyState:
    def update(self, game, current_time_ms: int, current_time_seconds: float) -> None:
        enter_button, back_button = game.multiplayer_lobby_view.draw(
            game.screen,
            game.multiplayer_status_text,
            game.multiplayer_error,
            pygame.mouse.get_pos(),
        )
        if game.multiplayer_ticket and current_time_ms - game.multiplayer_last_poll_ms >= 1000:
            game.multiplayer_last_poll_ms = current_time_ms
            self._poll_ticket(game)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._cancel_queue(game)
                game.close()
            if event.type == pygame.KEYDOWN:
                if event.key in {pygame.K_ESCAPE, pygame.K_q}:
                    self._cancel_queue(game)
                    game.state = GameState.EXPLORE
                elif event.key in {pygame.K_RETURN, pygame.K_SPACE}:
                    self._join_queue(game)
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = pygame.mouse.get_pos()
                if is_button_clicked(click_pos, enter_button):
                    self._join_queue(game)
                elif is_button_clicked(click_pos, back_button):
                    self._cancel_queue(game)
                    game.state = GameState.EXPLORE

    def _join_queue(self, game) -> None:
        if game.multiplayer_ticket is not None:
            return
        try:
            snapshot = game.multiplayer_serializer.snapshot_from_player(
                game.session.multiplayer_player_id,
                game.session.player_name,
                game.player,
            )
            game.multiplayer_ticket = game.multiplayer_gateway.enter_queue(snapshot)
            game.multiplayer_status_text = "Aguardando outro jogador entrar na fila..."
            game.multiplayer_error = None
            if game.multiplayer_ticket.match_id:
                self._open_match(game, game.multiplayer_ticket.match_id)
        except Exception as error:
            game.multiplayer_error = f"API indisponível em {API_CONFIG.base_url}. Verifique /health/ready."
            game.multiplayer_status_text = "Falha ao conectar no servidor online."
            print(f"[PokePY multiplayer] Falha ao entrar na fila: {error}")
            game.multiplayer_ticket = None

    def _poll_ticket(self, game) -> None:
        try:
            ticket = game.multiplayer_gateway.ticket_status(game.multiplayer_ticket.ticket_id)
            if ticket is None:
                game.multiplayer_error = "Ticket não encontrado. Tente entrar na fila novamente."
                game.multiplayer_ticket = None
                return
            game.multiplayer_ticket = ticket
            if ticket.status == MatchStatus.CANCELED:
                game.multiplayer_status_text = "Fila cancelada."
                game.multiplayer_ticket = None
            elif ticket.match_id:
                self._open_match(game, ticket.match_id)
        except Exception as error:
            game.multiplayer_error = "Falha ao consultar a fila multiplayer."
            print(f"[PokePY multiplayer] Falha ao consultar fila: {error}")

    def _open_match(self, game, match_id: str) -> None:
        match = game.multiplayer_gateway.read_match(match_id)
        if match is None:
            game.multiplayer_error = "Partida não encontrada."
            return
        game.multiplayer_match = match
        game.multiplayer_switch_mode = False
        game.multiplayer_error = None
        game.state = GameState.MULTIPLAYER_BATTLE

    def _cancel_queue(self, game) -> None:
        if game.multiplayer_ticket is None or game.multiplayer_ticket.match_id:
            return
        try:
            game.multiplayer_gateway.cancel_queue(
                game.multiplayer_ticket.ticket_id,
                game.session.multiplayer_player_id,
            )
        except Exception as error:
            print(f"[PokePY multiplayer] Falha ao cancelar fila: {error}")
        finally:
            game.multiplayer_ticket = None


class MultiplayerBattleState:
    def update(self, game, current_time_ms: int, current_time_seconds: float) -> None:
        if game.multiplayer_match is None:
            game.state = GameState.MULTIPLAYER_LOBBY
            return
        if current_time_ms - game.multiplayer_last_poll_ms >= 900:
            game.multiplayer_last_poll_ms = current_time_ms
            self._poll_match(game)
        controls = game.multiplayer_battle_view.draw(
            game.screen,
            game.multiplayer_match,
            game.session.multiplayer_player_id,
            game.multiplayer_switch_mode,
            pygame.mouse.get_pos(),
        )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._leave_match(game)
                game.close()
            if event.type == pygame.KEYDOWN:
                self._handle_key(game, event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_click(game, controls)

    def _poll_match(self, game) -> None:
        try:
            match = game.multiplayer_gateway.read_match(game.multiplayer_match.match_id)
            if match is not None:
                game.multiplayer_match = match
                self._sync_player(game)
        except Exception as error:
            game.multiplayer_error = "Falha ao atualizar a partida online."
            print(f"[PokePY multiplayer] Falha ao atualizar partida: {error}")

    def _handle_key(self, game, event) -> None:
        if event.key == pygame.K_ESCAPE:
            self._leave_match(game)
            game.state = GameState.EXPLORE
            return
        if game.multiplayer_match.status == MatchStatus.FINISHED and event.key in {pygame.K_RETURN, pygame.K_SPACE}:
            self._finish_screen(game)
            return
        if game.multiplayer_match.active_player_id != game.session.multiplayer_player_id:
            return
        player = self._local_snapshot(game)
        if player is None:
            return
        ready = player.normal_attack_count >= BATTLE_CONFIG.special_charge_required
        if event.key == pygame.K_z and not ready:
            self._send_action(
                game,
                MultiplayerActionType.ATTACK,
                {"attack_index": 0},
            )
        elif event.key == pygame.K_x and ready:
            self._send_action(
                game,
                MultiplayerActionType.ATTACK,
                {"attack_index": 1},
            )
        elif event.key == pygame.K_c:
            self._send_action(game, MultiplayerActionType.HEAL, {})
        elif event.key == pygame.K_v:
            game.multiplayer_switch_mode = not game.multiplayer_switch_mode

    def _handle_click(self, game, controls) -> None:
        click_pos = pygame.mouse.get_pos()
        if game.multiplayer_match.status == MatchStatus.FINISHED:
            if is_button_clicked(click_pos, controls.get("leave")):
                self._finish_screen(game)
            return
        if game.multiplayer_switch_mode:
            if is_button_clicked(click_pos, controls.get("back")):
                game.multiplayer_switch_mode = False
                return
            for rect, index in controls.get("team", []):
                if is_button_clicked(click_pos, rect):
                    self._send_action(
                        game,
                        MultiplayerActionType.SWITCH,
                        {"pokemon_index": index},
                    )
                    game.multiplayer_switch_mode = False
                    return
        if is_button_clicked(click_pos, controls.get("basic")):
            self._send_action(
                game,
                MultiplayerActionType.ATTACK,
                {"attack_index": 0},
            )
        elif is_button_clicked(click_pos, controls.get("special")):
            self._send_action(
                game,
                MultiplayerActionType.ATTACK,
                {"attack_index": 1},
            )
        elif is_button_clicked(click_pos, controls.get("heal")):
            self._send_action(game, MultiplayerActionType.HEAL, {})
        elif is_button_clicked(click_pos, controls.get("switch")):
            game.multiplayer_switch_mode = True
        elif is_button_clicked(click_pos, controls.get("leave")):
            self._leave_match(game)
            game.state = GameState.EXPLORE

    def _send_action(self, game, action_type, payload) -> None:
        if (
            game.multiplayer_match is None
            or game.multiplayer_match.active_player_id != game.session.multiplayer_player_id
        ):
            return
        try:
            action = MultiplayerAction(
                game.multiplayer_match.match_id,
                game.session.multiplayer_player_id,
                action_type,
                payload,
            )
            game.multiplayer_match = game.multiplayer_gateway.send_action(action)
            game.multiplayer_error = None
            self._sync_player(game)
            game.save_progress()
        except Exception as error:
            game.multiplayer_error = "Não foi possível enviar a ação para a API."
            print(f"[PokePY multiplayer] Falha ao enviar ação: {error}")

    def _leave_match(self, game) -> None:
        if game.multiplayer_match is None:
            return
        try:
            game.multiplayer_match = game.multiplayer_gateway.leave_match(
                game.multiplayer_match.match_id,
                game.session.multiplayer_player_id,
            )
            self._sync_player(game)
            game.save_progress()
        except Exception as error:
            print(f"[PokePY multiplayer] Falha ao sair da partida: {error}")

    def _finish_screen(self, game) -> None:
        self._sync_player(game)
        game.save_progress()
        game.multiplayer_ticket = None
        game.multiplayer_match = None
        game.multiplayer_switch_mode = False
        game.multiplayer_error = None
        game.state = GameState.EXPLORE

    def _sync_player(self, game) -> None:
        snapshot = self._local_snapshot(game)
        if snapshot is not None:
            game.multiplayer_serializer.apply_snapshot_to_player(
                snapshot,
                game.player,
            )

    def _local_snapshot(self, game):
        if game.multiplayer_match is None:
            return None
        return next(
            (
                player
                for player in game.multiplayer_match.players
                if player.player_id == game.session.multiplayer_player_id
            ),
            None,
        )
