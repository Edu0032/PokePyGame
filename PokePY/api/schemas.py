from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    status: str
    database: str


class LeaderboardEntryCreate(BaseModel):
    player_name: str = Field(min_length=1, max_length=80)
    elapsed_seconds: int = Field(ge=0)


class LeaderboardEntryResponse(BaseModel):
    player_name: str
    elapsed_seconds: int
    created_at: str


class LeaderboardSaveResponse(BaseModel):
    entry: LeaderboardEntryResponse
    position: int | None


class LeaderboardPageResponse(BaseModel):
    items: list[LeaderboardEntryResponse]
    limit: int
    offset: int
    returned: int


class PokemonProgressPayload(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    type: str = Field(min_length=1, max_length=40)
    level: int = Field(ge=1)
    hp: int = Field(ge=0)
    max_hp: int = Field(ge=1)
    xp: int = Field(ge=0)
    attacks: list[str] = Field(default_factory=list)
    evolution_stage: int = Field(ge=0)


class PlayerProgressPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    player_id: str = Field(min_length=1, max_length=80)
    player_name: str = Field(min_length=1, max_length=80)
    zone_index: int = Field(ge=0)
    x: int = Field(ge=0)
    y: int = Field(ge=0)
    items: dict[str, int] = Field(default_factory=dict)
    team: list[PokemonProgressPayload] = Field(default_factory=list)


class PlayerProgressSaveResponse(BaseModel):
    saved: bool
    progress: PlayerProgressPayload


class MultiplayerCapabilitiesResponse(BaseModel):
    status: str
    prepared_contracts: list[str]
    available_endpoints: list[str]


class MultiplayerPokemonPayload(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    type: str = Field(min_length=1, max_length=40)
    level: int = Field(ge=1)
    hp: int = Field(ge=0)
    max_hp: int = Field(ge=1)
    xp: int = Field(ge=0)
    attacks: list[str] = Field(default_factory=list)
    evolution_stage: int = Field(ge=0)


class MultiplayerPlayerPayload(BaseModel):
    player_id: str = Field(min_length=1, max_length=80)
    player_name: str = Field(min_length=1, max_length=80)
    team: list[MultiplayerPokemonPayload] = Field(min_length=1)
    active_pokemon_index: int = Field(default=0, ge=0)
    items: dict[str, int] = Field(default_factory=dict)
    normal_attack_count: int = Field(default=0, ge=0)


class MatchmakingJoinRequest(BaseModel):
    player: MultiplayerPlayerPayload


class CancelMatchmakingRequest(BaseModel):
    player_id: str = Field(min_length=1, max_length=80)


class MatchTicketResponse(BaseModel):
    ticket_id: str
    player_id: str
    status: str
    match_id: str | None = None


class MatchSnapshotResponse(BaseModel):
    match_id: str
    status: str
    players: list[MultiplayerPlayerPayload]
    active_player_id: str | None = None
    winner_player_id: str | None = None
    turn_number: int
    events: list[str]


class MultiplayerActionRequest(BaseModel):
    player_id: str = Field(min_length=1, max_length=80)
    action_type: str = Field(pattern="^(attack|switch|heal|flee)$")
    payload: dict = Field(default_factory=dict)
    action_id: str | None = Field(default=None, min_length=1, max_length=80)


class MultiplayerActionResponse(BaseModel):
    accepted: bool
    match: MatchSnapshotResponse


class LeaveMatchRequest(BaseModel):
    player_id: str = Field(min_length=1, max_length=80)
