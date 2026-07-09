from uuid import uuid4

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from PokePY.api.converters import match_snapshot_response, match_ticket_response, multiplayer_player_from_payload
from PokePY.api.schemas import (
    LeaveMatchRequest,
    MatchSnapshotResponse,
    MatchTicketResponse,
    MatchmakingJoinRequest,
    MultiplayerActionRequest,
    MultiplayerActionResponse,
    MultiplayerCapabilitiesResponse,
)
from PokePY.services.multiplayer_contracts import MultiplayerAction, MultiplayerActionType
from PokePY.services.multiplayer_errors import InvalidTurnError, MatchNotFoundError, PlayerNotInMatchError
from PokePY.services.multiplayer_service import MultiplayerService


def create_multiplayer_router(multiplayer_service: MultiplayerService) -> APIRouter:
    router = APIRouter(prefix="/multiplayer", tags=["multiplayer"])

    @router.get("/capabilities", response_model=MultiplayerCapabilitiesResponse)
    def multiplayer_capabilities() -> MultiplayerCapabilitiesResponse:
        return MultiplayerCapabilitiesResponse(
            status="enabled",
            prepared_contracts=[
                "PlayerSnapshot",
                "PokemonSnapshot",
                "MatchTicket",
                "MatchSnapshot",
                "MultiplayerAction",
                "MultiplayerGateway",
            ],
            planned_endpoints=[
                "POST /multiplayer/matchmaking/join",
                "GET /multiplayer/matchmaking/status/{ticket_id}",
                "GET /multiplayer/matches/{match_id}",
                "POST /multiplayer/matches/{match_id}/actions",
                "POST /multiplayer/matches/{match_id}/leave",
            ],
        )

    @router.post("/matchmaking/join", response_model=MatchTicketResponse, status_code=status.HTTP_201_CREATED)
    def join_matchmaking(payload: MatchmakingJoinRequest) -> MatchTicketResponse:
        try:
            ticket = multiplayer_service.enter_queue(multiplayer_player_from_payload(payload.player))
        except SQLAlchemyError as error:
            raise HTTPException(status_code=503, detail="Não foi possível entrar na fila multiplayer.") from error
        return match_ticket_response(ticket)

    @router.get("/matchmaking/status/{ticket_id}", response_model=MatchTicketResponse)
    def matchmaking_status(ticket_id: str) -> MatchTicketResponse:
        try:
            ticket = multiplayer_service.ticket_status(ticket_id)
        except SQLAlchemyError as error:
            raise HTTPException(status_code=503, detail="Não foi possível consultar a fila multiplayer.") from error
        if ticket is None:
            raise HTTPException(status_code=404, detail="Ticket não encontrado.")
        return match_ticket_response(ticket)

    @router.get("/matches/{match_id}", response_model=MatchSnapshotResponse)
    def get_match(match_id: str) -> MatchSnapshotResponse:
        try:
            match = multiplayer_service.read_match(match_id)
        except SQLAlchemyError as error:
            raise HTTPException(status_code=503, detail="Não foi possível carregar a partida multiplayer.") from error
        if match is None:
            raise HTTPException(status_code=404, detail="Partida não encontrada.")
        return match_snapshot_response(match)

    @router.post("/matches/{match_id}/actions", response_model=MultiplayerActionResponse)
    def send_action(match_id: str, payload: MultiplayerActionRequest) -> MultiplayerActionResponse:
        try:
            match = multiplayer_service.send_action(
                MultiplayerAction(
                    match_id=match_id,
                    player_id=payload.player_id,
                    action_type=MultiplayerActionType(payload.action_type),
                    payload=payload.payload,
                    action_id=payload.action_id or uuid4().hex,
                )
            )
        except MatchNotFoundError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
        except (InvalidTurnError, PlayerNotInMatchError) as error:
            raise HTTPException(status_code=409, detail=str(error)) from error
        except SQLAlchemyError as error:
            raise HTTPException(status_code=503, detail="Não foi possível registrar a ação multiplayer.") from error
        return MultiplayerActionResponse(accepted=True, match=match_snapshot_response(match))

    @router.post("/matches/{match_id}/leave", response_model=MatchSnapshotResponse)
    def leave_match(match_id: str, payload: LeaveMatchRequest) -> MatchSnapshotResponse:
        try:
            match = multiplayer_service.leave_match(match_id, payload.player_id)
        except MatchNotFoundError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
        except SQLAlchemyError as error:
            raise HTTPException(status_code=503, detail="Não foi possível sair da partida multiplayer.") from error
        return match_snapshot_response(match)

    return router
