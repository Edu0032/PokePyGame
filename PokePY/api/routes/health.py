from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from PokePY.api.schemas import HealthResponse


def create_health_router(engine: Engine | None = None) -> APIRouter:
    router = APIRouter(tags=["health"])

    @router.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        return HealthResponse(status="ok", database="configured")

    @router.get("/health/ready", response_model=HealthResponse)
    def readiness() -> HealthResponse:
        if engine is None:
            return HealthResponse(status="ok", database="not_attached")
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
        except SQLAlchemyError as error:
            raise HTTPException(status_code=503, detail="Database is not ready.") from error
        return HealthResponse(status="ok", database="ready")

    return router
