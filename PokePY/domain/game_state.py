from enum import StrEnum


class GameState(StrEnum):
    PLAYER_NAME = "player_name"
    SELECT_TEAM = "select_team"
    EXPLORE = "explore"
    INVENTORY = "inventory"
    BATTLE = "battle"
    SELECT_IN_BATTLE = "select_in_battle"
    GAME_OVER = "game_over"
    LEADERBOARD = "leaderboard"
    RANKING = "ranking"
    MULTIPLAYER_LOBBY = "multiplayer_lobby"
    MULTIPLAYER_BATTLE = "multiplayer_battle"


class BattleResult(StrEnum):
    WIN = "win"
    LOSE = "lose"
    FLED = "fled"
    FLEE_BLOCKED = "flee_blocked"
    SWITCH_REQUIRED = "switch_required"
    SWITCH_REQUESTED = "switch_requested"
