from datetime import datetime, timezone

from sqlalchemy.orm import sessionmaker

from PokePY.domain.models import Player
from PokePY.infrastructure.sqlalchemy.models import PlayerProgressRecord
from PokePY.services.player_progress_service import PlayerProgress, PlayerProgressService

class SQLAlchemyPlayerProgressRepository:
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory
        self.serializer = PlayerProgressService(self)

    def save(self, player_id: str, player: Player) -> None:
        progress = self.serializer.to_progress(player_id, player_id, player)
        self.save_progress(progress)

    def load(self, player_id: str) -> Player | None:
        progress = self.load_progress(player_id)
        return self.serializer.from_progress(progress) if progress else None

    def save_progress(self, progress: PlayerProgress) -> PlayerProgress:
        payload = self.serializer.to_dict(progress)
        with self.session_factory() as session:
            record = session.get(PlayerProgressRecord, progress.player_id)
            if record is None:
                record = PlayerProgressRecord(
                    player_id=progress.player_id,
                    player_name=progress.player_name,
                    zone_index=progress.zone_index,
                    x=progress.x,
                    y=progress.y,
                    items=payload["items"],
                    team=payload["team"],
                    updated_at=datetime.now(timezone.utc),
                )
                session.add(record)
            else:
                record.player_name = progress.player_name
                record.zone_index = progress.zone_index
                record.x = progress.x
                record.y = progress.y
                record.items = payload["items"]
                record.team = payload["team"]
                record.updated_at = datetime.now(timezone.utc)
            session.commit()
        return progress

    def load_progress(self, player_id: str) -> PlayerProgress | None:
        with self.session_factory() as session:
            record = session.get(PlayerProgressRecord, player_id)
            if record is None:
                return None
            return self.serializer.from_dict(
                {
                    "player_id": record.player_id,
                    "player_name": record.player_name,
                    "zone_index": record.zone_index,
                    "x": record.x,
                    "y": record.y,
                    "items": record.items,
                    "team": record.team,
                }
            )
