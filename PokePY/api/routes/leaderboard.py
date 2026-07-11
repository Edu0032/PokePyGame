from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy.exc import SQLAlchemyError

from PokePY.api.converters import leaderboard_response
from PokePY.api.schemas import (
    LeaderboardEntryCreate,
    LeaderboardEntryResponse,
    LeaderboardPageResponse,
    LeaderboardSaveResponse,
)
from PokePY.services.leaderboard_service import LeaderboardService


def create_leaderboard_router(leaderboard_service: LeaderboardService) -> APIRouter:
    router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])

    @router.post("", response_model=LeaderboardSaveResponse, status_code=status.HTTP_201_CREATED)
    def create_leaderboard_entry(payload: LeaderboardEntryCreate) -> LeaderboardSaveResponse:
        try:
            result = leaderboard_service.register_completion(payload.player_name, payload.elapsed_seconds)
        except SQLAlchemyError as error:
            raise HTTPException(status_code=503, detail="Não foi possível salvar o placar.") from error
        return LeaderboardSaveResponse(entry=leaderboard_response(result.entry), position=result.position)

    @router.get("", response_model=list[LeaderboardEntryResponse])
    def list_leaderboard(limit: int = Query(default=10, ge=1, le=100)) -> list[LeaderboardEntryResponse]:
        try:
            entries = leaderboard_service.top_scores(limit)
        except SQLAlchemyError as error:
            raise HTTPException(status_code=503, detail="Não foi possível carregar o placar.") from error
        return [leaderboard_response(entry) for entry in entries]

    @router.get("/page", response_model=LeaderboardPageResponse)
    def paginated_leaderboard(
        limit: int = Query(default=10, ge=1, le=100),
        offset: int = Query(default=0, ge=0, le=1000),
    ) -> LeaderboardPageResponse:
        try:
            entries = leaderboard_service.top_scores(limit + offset)[offset : offset + limit]
        except SQLAlchemyError as error:
            raise HTTPException(status_code=503, detail="Não foi possível carregar o placar.") from error
        return LeaderboardPageResponse(
            items=[leaderboard_response(entry) for entry in entries],
            limit=limit,
            offset=offset,
            returned=len(entries),
        )

    return router
