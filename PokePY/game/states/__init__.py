from PokePY.domain.game_state import GameState
from PokePY.game.states.battle_state import BattleState, PokemonSwitchState
from PokePY.game.states.exploration_state import ExplorationState
from PokePY.game.states.inventory_state import InventoryState
from PokePY.game.states.leaderboard_state import (
    GameOverState,
    LeaderboardState,
    RankingBrowserState,
)
from PokePY.game.states.multiplayer_state import (
    MultiplayerBattleState,
    MultiplayerLobbyState,
)
from PokePY.game.states.player_name_state import PlayerNameState
from PokePY.game.states.team_selection_state import TeamSelectionState


def build_state_handlers():
    return {
        GameState.PLAYER_NAME: PlayerNameState(),
        GameState.SELECT_TEAM: TeamSelectionState(),
        GameState.EXPLORE: ExplorationState(),
        GameState.INVENTORY: InventoryState(),
        GameState.BATTLE: BattleState(),
        GameState.SELECT_IN_BATTLE: PokemonSwitchState(),
        GameState.GAME_OVER: GameOverState(),
        GameState.LEADERBOARD: LeaderboardState(),
        GameState.RANKING: RankingBrowserState(),
        GameState.MULTIPLAYER_LOBBY: MultiplayerLobbyState(),
        GameState.MULTIPLAYER_BATTLE: MultiplayerBattleState(),
    }
