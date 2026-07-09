from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from PokePY.api.converters import progress_from_payload, progress_response
from PokePY.api.schemas import PlayerProgressPayload, PlayerProgressSaveResponse


def create_progress_router(progress_repository) -> APIRouter:
    router = APIRouter(prefix="/players", tags=["players"])

    @router.put("/{player_id}/progress", response_model=PlayerProgressSaveResponse)
    def save_player_progress(player_id: str, payload: PlayerProgressPayload) -> PlayerProgressSaveResponse:
        if player_id != payload.player_id:
            raise HTTPException(status_code=400, detail="O player_id da URL precisa ser igual ao player_id do corpo.")
        progress = progress_from_payload(payload)
        try:
            saved_progress = progress_repository.save_progress(progress)
        except AttributeError as error:
            raise HTTPException(status_code=501, detail="Repositório de progresso não suporta payload serializado.") from error
        except SQLAlchemyError as error:
            raise HTTPException(status_code=503, detail="Não foi possível salvar o progresso.") from error
        return PlayerProgressSaveResponse(saved=True, progress=progress_response(saved_progress))

    @router.get("/{player_id}/progress", response_model=PlayerProgressPayload)
    def load_player_progress(player_id: str) -> PlayerProgressPayload:
        try:
            progress = progress_repository.load_progress(player_id)
        except AttributeError as error:
            raise HTTPException(status_code=501, detail="Repositório de progresso não suporta payload serializado.") from error
        except SQLAlchemyError as error:
            raise HTTPException(status_code=503, detail="Não foi possível carregar o progresso.") from error
        if progress is None:
            raise HTTPException(status_code=404, detail="Progresso do jogador não encontrado.")
        return progress_response(progress)

    return router
