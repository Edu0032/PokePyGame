from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from PokePY.infrastructure.sqlalchemy.models import LeaderboardScoreRecord
from PokePY.services.leaderboard_contracts import LeaderboardEntry


class SQLAlchemyLeaderboardRepository:
    def __init__(self, session_factory: sessionmaker, max_entries: int = 100):
        self.session_factory = session_factory
        self.max_entries = max_entries

    def save_score(self, entry: LeaderboardEntry) -> LeaderboardEntry:
        created_at = self._parse_datetime(entry.created_at)
        with self.session_factory() as session:
            record = LeaderboardScoreRecord(
                player_name=entry.player_name,
                elapsed_seconds=entry.elapsed_seconds,
                created_at=created_at,
            )
            session.add(record)
            session.commit()
            session.refresh(record)
            self._trim_scores(session)
            session.commit()
            return self._entry_from_record(record)

    def top_scores(self, limit: int = 10) -> list[LeaderboardEntry]:
        safe_limit = max(0, int(limit))
        statement = (
            select(LeaderboardScoreRecord)
            .order_by(
                LeaderboardScoreRecord.elapsed_seconds.asc(),
                LeaderboardScoreRecord.created_at.asc(),
                LeaderboardScoreRecord.player_name.asc(),
            )
            .limit(safe_limit)
        )
        with self.session_factory() as session:
            records = session.execute(statement).scalars().all()
            return [self._entry_from_record(record) for record in records]

    def _trim_scores(self, session) -> None:
        if self.max_entries <= 0:
            return
        statement = (
            select(LeaderboardScoreRecord.id)
            .order_by(
                LeaderboardScoreRecord.elapsed_seconds.asc(),
                LeaderboardScoreRecord.created_at.asc(),
                LeaderboardScoreRecord.player_name.asc(),
            )
            .offset(self.max_entries)
        )
        stale_ids = [row[0] for row in session.execute(statement).all()]
        if not stale_ids:
            return
        for score_id in stale_ids:
            record = session.get(LeaderboardScoreRecord, score_id)
            if record is not None:
                session.delete(record)

    def _entry_from_record(self, record: LeaderboardScoreRecord) -> LeaderboardEntry:
        created_at = record.created_at
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=UTC)
        return LeaderboardEntry(
            player_name=record.player_name,
            elapsed_seconds=record.elapsed_seconds,
            created_at=created_at.astimezone(UTC).isoformat(timespec="seconds"),
        )

    def _parse_datetime(self, value: str) -> datetime:
        try:
            parsed = datetime.fromisoformat(value)
        except ValueError:
            parsed = datetime.now(UTC)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=UTC)
        return parsed.astimezone(UTC)
